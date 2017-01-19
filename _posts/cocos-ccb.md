---
title: cocos之使用ccb的一些坑
date: 2017-01-12 10:46:22
tags: cocos
---
cocosBuilder是一款很老的编辑器了，所以如果还在使用的话，需要注意一些坑。

#### 1.labelttf不是labelttf
通过查看源代码，以及查看成员方法，可以得出，ccb将LabelTTF解析成了Label，所以在ccb中创建的Labelttf，代码中只能调用Label的方法，像setFontFillColor等LabelTTF的方法都是不能使用的。

虽然Label上有一个方法setTextColor可以设置颜色，但如果使用，会发现最终显示的颜色与设定的颜色并不一致，它将你在ccb里给他设定的初始颜色做了混合，如果想要生效，那要么在ccb里设成白色，要么在代码中调setTextColor前，先调用setColor(cc.color.WHITE)

同样，setFontSize是LabelTTF上的方法，代码中不能使用，办法是使用Label上的setSystemFontSize方法来代替。当然，最彻底的解决办法就是修改ccb的解析代码，它位于editor-support/cocosbuilder/ccLabelTTFLoader.h中

#### 2.一个ccb中最好不要有多个动画
我们一般调用

```
animationManager.runAnimationsForSequenceNamedTweenDuration();
```
来播放动画，这个方法一上来就会把现有的动画都停止掉，所以如果一个界面有多个动画，最好不要放在同一个ccb里，否则一旦需要同时播放的时候，正在播放中的动画就会被停止

#### 3.owner最好不要重用，方法绑定在owner或者documentRoot上，在load之前必须先设置

cc.BuilderReader.load方法第二个参数为owner，它用于寻找ccb中设定的属性和方法。owner最好不要重用，否则会出现各种奇怪的现象。例如我们需要加载一个子ccb时，可以新建一个node作为owner来使用。

```
var delegate = new cc.Node();	//用来做ower
delegate.retain();
delegate._finishAction = function(){
	node.removeFromParent();
	delegate.release();
}

var node = cc.BuilderReader.load(name, delegate);
//owner必须继承自node
```
另外回调必须在调用load之前绑定好,这里_finishAction就是绑定的回调，虽然回调的时机在初始化以后，但如果不先设置，那么在解析的时候找不到接口，会导致绑定不成功

#### 4.不能在tableCellTouched中移除界面
这个与ccb没有关系，顺便提醒一下。我们经常有点击后关闭界面的需求，在别的情况下可能不会出什么问题，但如果在tableView的tableCellTouched回调中移除，会发生崩溃。因为在这个回调之后，touchEnd其实还没有结束，还会继续处理scroll上的一些代码，如果移除掉了根节点，导致内存被释放，那后续的代码就崩溃了