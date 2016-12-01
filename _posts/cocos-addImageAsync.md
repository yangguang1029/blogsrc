---
title: cocos-addImageAsync解析
date: 2016-11-25 11:44:28
tags: cocos
---

当我们在cocos内需要做一些比较耗性能的事情时，我们可以一些很巧妙地方案，例如开启多线程，以及将任务分解到每一帧完成一部分。在TextureCache的addImageAsync方法里，就同时用到了这两种办法，把这部分源码看明白，对自己实现能有很大的帮助

类TextureCache维护一个队列_asyncStructQueue，它存放需要执行的任务，这些任务将在异步线程执行，加载生成Image类

```
std::queue<AsyncStruct*>* _asyncStructQueue;
```
一个双向队列_imageInfoQueue,他存放加载好的Image，这些加载好的图片资源就会每帧从队列中获取一个，用来生成纹理Texture2D，生成好的纹理就可以在游戏内直接使用了

```
std::deque<ImageInfo*>* _imageInfoQueue;
```
这两个队列都是先进先出的操作，我也不是很明白为什么要用deque，有知道的可以告诉我一下。然后这两个队列因为都需要在异步线程操作，所以操作时需要用锁锁住。

使用一个_asyncRefCount来记录当前任务的数量，当往_asyncStructQueue添加一个任务asyncStruct时，计数+1，当一个纹理生成完成，销毁该任务asyncStruct，计数-1

```
int _asyncRefCount;
```

### 入口
需要异步加载一个图片时，首先调用

```
void TextureCache::addImageAsync(const std::string &path, const std::function<void(Texture2D*)>& callback)
```
首先判断一下这个path对应的texture是否已经在缓存里，如果在，则直接返回。否则如果_asyncStructQueue还未初始化，则执行初始化，然后生成一个AsyncStruct加入队列_asyncStructQueue中。

### 异步线程
类TextureCache维护一个异步线程，这个线程在_asyncStructQueue初始化时开启

```
std::thread* _loadingThread;
```
在这个线程执行的函数是

```
void TextureCache::loadImage()
```
这个线程通过std::condition_variable _sleepCondition来唤醒和休眠，当有任务加入任务队列_asyncStructQueue时，唤醒线程执行loadImage函数，在这个函数里发现_asyncStructQueue被清空时，休眠这个线程。

在执行loadImage时，会先看一下需要加载的图片是否已经在处理队列_imageInfoQueue中了。如果不在，则生成一个新的Image，执行

```
image->initWithImageFileThreadSafe(filename)
```
如果initWithImageFileThreadSafe返回true，则表示这张图片资源加载成功了，用这个image生成一个imageInfo放到_imageInfoQueue里。

### 定时回调
这个定时回调每帧都会被调用一次，它将上一步生成的image变成Texture2D。当_asyncRefCount从0变为1时，表示开始有任务需要完成，开启这个定时器，当_asyncRefCount变为0时表示任务全部完成，这个定时器会被关闭。

```
Director::getInstance()->getScheduler()->schedule(CC_SCHEDULE_SELECTOR(TextureCache::addImageAsyncCallBack), this, 0, false);
```
定时执行的函数就是addImageAsyncCallBack了，在这个函数里，通过

```
texture->initWithImage(image);
```
生成Texture2d，并存在缓存里，每次通过TextureCache加载纹理的时候，都会先看看是否已经存在缓存里了。
到这里，这个任务就完成了，执行下回调函数，然后把_asyncRefCount减一，搞定了


