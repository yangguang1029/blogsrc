---
title: js对象与继承(二)
date: 2016-11-18 16:33:43
tags: javaScript
---

### 类继承与原型继承
先分别举个例子吧，首先是原型继承

```
var proto = {"a":1,"b":{"c":2}}
var f1 = function(){}
var f2 = function(){}
f1.prototype = proto
f2.prototype = proto
var t1 = new f1()
var t2 = new f2()
```
其次是类继承

```
var proto = function(){
		this.a = 1;
		this.b = {"c":2};
	}
var f1 = function(){}
var f2 = function(){}
f1.prototype = new proto()
f2.prototype = new proto()
var t1 = new f1()
var t2 = new f2()
```
它们的区别就在于，类继承先定义了一个基类proto，在继承时，子类构造函数的prototype是根据这个基类new出来的一个对象。

这两种方式各有优劣:

正如上一篇说到的，如果执行代码

```
t1.b.c = 12
console.log(t2.b.c)
```
对于原型继承，因为proto被改变了，所以t2.b.c也变成了12，而对于类继承则不会有问题，这对于不够熟悉js的人来说绝对是个坑。

不过原型继承实现起来比类继承要更灵活，因为不需要做抽象基类的工作，但如果随意地使用原型继承，例如用作prototype的对象是一个非常庞大复杂的对象，那显然会产生问题。