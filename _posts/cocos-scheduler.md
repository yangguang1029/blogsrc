---
title: cocos之定时器scheduler
date: 2017-03-21 17:51:53
tags: cocos
---
游戏中经常需要用到定时器，定时循环执行某个任务n次，或者延迟一段时间后执行某个任务，此时需要用到的类是Scheduler。它的原理和使用并不复杂，本文记录一些细节问题。

### 使用
使用起来非常简单，首先通过Director获取Scheduler对象，然后调用它的schedule方法，参数依次为回调函数，回调函数对象，回调周期，回调次数，第一次回调延迟，是否暂停等待。

```
Scheduler::schedule(SEL_SCHEDULE selector, Ref *target, float interval, unsigned int repeat, float delay, bool paused)
```

此外还有一个接口

```
void scheduleUpdate(T *target, int priority, bool paused)
```
它可以设定优先级priority，优先级越低，越早被调用。注册的对象target的update方法会被调用。

在CCNode里预先封装了一个函数

```
void Node::scheduleUpdate()
```
它就是通过上面scheduleUpdate实现的，其priority为0。如果我们调用它,则Node内的update方法会每帧被调用一次。

### 实现原理
定时器scheduler的实现原理很简单，它的update方法每帧都会被调用，此时查看所有注册了的定时器，如果满足触发条件，则触发一次，然后触发次数加1，触发次数达到注册时的次数，则结束并销毁这个定时器。

### 注意事项
1. schedule方法，定时器的回调次数比参数repeat多1，也就是说如果希望只回调一次，repeat应该设为0.以此内推
2. 通过schedule方法，同一个类注册的定时器，先注册者先回调
3. 通过schedule方法，不同类注册的定时器，每个类的定时器会按上一条规则全部执行完，然后再执行下一个类的全部回调。不同类之间按照注册时先后顺序来，先注册的类先回调
4. 通过scheduleUpdate注册的定时器，根据priority排序，priority越小越先被调用
5. 定时器的回调都有一个参数float t，它表示当前与上一次回调的时间间隔，引擎无法确保两次回调的间隔一定是我们在schedule时设定的间隔，或者我们预计的每帧间隔。
6. 如果需要将定时器加速或者减速，可以使用Scheduler::setTimeScale方法。设一个小于1的值，回调频率将会变慢，设一个大于1的值，回调频率会变快，但需要注意回调时参数t不会改变


