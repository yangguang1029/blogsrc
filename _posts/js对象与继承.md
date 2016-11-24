---
title: js对象与继承(一)
date: 2016-11-18 11:24:32
tags: javaScript
---

大家都知道在js中创建一个对象的一种很基本的方式

```
function f(){
	this.a = 1;
}
var test = new f();
```

当执行new的时候，系统实际做的事情分了几步

1. var obj = Object.create(f.prototype)
2. var result = f.call(obj)
3. result && typeof result === 'object' ? return result : return obj

用语言描述就是，首先用f.prototype构造一个Object，这里命名为obj，然后将obj作为参数this去调用构造函数f，返回值为result，如果result是一个对象，则返回它，也就意味着test = result，否则 test = obj。

然后再看prototype是什么东西吧，举个例子

```
var p = {"a":1, "b":{"c":2}}
var f = function(){this.d = 3}
f.prototype = p
var t = new f()
console.log(t.d)
console.log(t.a)

```
这里p是一个对象，f是一个构造函数，将f的prototype设为p，当使用f构造出一个对象t出来时，t会有一个属性\_\_proto__,它就指向了p

当我们获取t.d时，t是有d属性的，这个没问题
当我们获取t.a时，t没有a属性，此时会沿着它的原型链往上查找，也就是查找它的\_\_proto__，也就是p，p是有a属性的，所以将a的值返回。我们可以使用Object类上的一个方法hasOwnProperty来判断一个属性或方法是对象本身的，还是原型链上的。例如

```
console.log(t.hasOwnProperty("a"))	//false
console.log(t.hasOwnProperty("d"))	//true
```
上面说的是取值，赋值的时候就稍微复杂些，例如

```
t.a = 11;
t.b.c = 12
```
执行第一句话，也就是对于基础数据类型，在chrome控制台上可以看到t的属性列表里出现了a并且值为11，而p的a仍然是1不变。也就是对原型上的基础数据类型赋值，不会影响原型，而是自身多了一个这样的属性。但使用hasOwnProperty看，仍然为false，这应该是js的一些不完善的地方吧。

执行第二句话，可以看到p的b变成了{"c":12}，也就是修改原型链上的非基础数据类型，会改变原型链本身。这也是javascript中使用类继承比使用原型继承更好的原因之一。下篇再分别讲这两种继承方式