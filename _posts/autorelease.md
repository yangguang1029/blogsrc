---
title: cocos tips 之autorelease
date: 2016-11-14 21:03:49
tags: cocos
---

首先autorelease是个怎么回事呢？引用计数的原理就不用说了，凡是继承自Ref的类new出得对象，都使用引用计数来进行内存管理。对象被new出来时，初始引用计数为1，每次被retain时，引用计数+1，被release时，引用计数-1。当引用计数降为0时，则执行析构函数，内存被回收。
所以retain必须和release成对出现，才能避免内存泄漏(例如被加到父容器和从父容器移除时，就分别执行了retain和release)，而且最初的new也必须对应一次release，例如

```
Node* node = new Node();	//引用计数1
this->addChild(node);	//引用计数2
```
之后在合适的时候移除

```
node->removeFromParent();	//引用计数1
```
可见，此时如果不再执行一次release的话，引用计数一直为1，内存得不到释放，内存就泄漏了。对于一个被引用了很多的对象，要找到最终执行release的时机，显然很难，autoRelease就是为了解决这个问题的，当执行autoRelease函数时，这个对象将会被加到一个autoreleasePool中（并不会执行retain），在这帧结束时，这个pool内所有Ref对象都会执行一次release，这次release就抵消掉了new时候的那个引用计数，因此只要保证其他引用它的地方retain和release成对，就可以保证内存不会泄露。

除了使用系统自带的

```
PoolManager::getInstance()->getCurrentPool()
```
外，也可以自己新建一个autoRelease，因为要确保执行析构函数，所以不建议使用new来构造，直接在栈上创造一个即可，例如

```
AutoreleasePool p;
p.addObject(obj)
```
当退出执行函数时，p会被析构，此时所有被加入的Ref对象都会被执行一次release。什么时候需要自己新建一个autoreleasePool来使用呢，例如一帧内生成了大量autorelease对象（通常在循环中），如果使用默认的autoreleasePool，则全部集中在这帧结束时释放，可能导致性能降低，此时可以手动创建一个autoreleasePool来进行管理。
