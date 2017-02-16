---
title: cocos之Scene的切换
date: 2017-02-04 15:44:35
tags: cocos
---

场景切换，牵涉到的是老scene善后处理和新scene的初始化，如果对各个函数调用的先后顺序不明的话，可能就会出问题(例如注册监听和取消监听，一般都写在onEnter和onExit方法内)

涉及到scene切换的方法，都在director内,常用的为

```
void Director::runWithScene(Scene *scene)
void Director::replaceScene(Scene *scene)
```
Director内通过\_scenesStack， \_runningScene，\_nextScene进行管理。每帧都会调用drawScene方法，这个方法里，有一段代码。

```
 /* to avoid flickr, nextScene MUST be here: after tick and before draw.
     */
    if (_nextScene)
    {
        setNextScene();
    }
```
这里还有一些注释，说明了切换scene的操作，在老scene的事件都处理完了之后，渲染新scene之前。这里setNextScene就是执行了切换scene的逻辑。

scene的切换分为有渐变和没有渐变两种情况

- 没有渐变的时候，切换的回调会直接调用,具体可以看源代码。顺序为

```
_runningScene->onExitTransitionDidStart();
_runningScene->onExit();
//此时_runningScene已经指向了新scene
_runningScene->onEnter();
_runningScene->onEnterTransitionDidFinish();
```

- 有渐变的情况其实也简单，渐变的效果是通过TransitionScene类来实现的，它将新scene存为\_inScene, 需要被替换掉的老scene存为\_outScene，然后它的draw函数会同时渲染这两个scene。为了将逻辑与视觉效果相符，新旧scene的执行回调也发生了变化，老scene的onExit延迟到新scene进场完毕后才调用

```
_outScene->onExitTransitionDidStart();
_inScene->onEnter();

_outScene->onExit();
_inScene->onEnterTransitionDidFinish();
```
关于TransitionScene的一些细节:

- TransitionScene的各个子类,都只是实现了进场动画，并没有哪个实现有离场动画
- TransitionScene的finish回调中会执行director->replaceScene(\_inScene);设置真正的新scene。Director::setNextScene方法里，runningIsTransition只有在这时候才可能为true,否则如果老scene是个TransitionScene，意味着进场动画还没有结束，node的\_running为true,此时不运行进行切换的,强制切换会触发assert。
- 不要妄想使用连环Transition，原因和上面一样，进场动画还没执行完就切换scene，例如

```
TransitionFade* fade = TransitionFade::create(2, scene, Color3B::GREEN);
TransitionFade* fade1 = TransitionFade::create(2, fade, Color3B::GREEN);
TransitionFade* fade2 = TransitionFade::create(2, fade1, Color3B::GREEN);
Director::getInstance()->replaceScene(fade2);
```

