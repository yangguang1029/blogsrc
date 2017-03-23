---
title: javaScript之this
date: 2017-03-23 15:50:39
tags: javascript
---
js中的this，很容易让刚接触的人摸不着头脑，但其实主要明白了怎么回事，也不会很复杂。函数里的this指向什么，跟它的当前执行环境有关。

我们从简单到复杂，通过一些例子来说明

```
var A = function(){
	console.log(this);
}
var a = new A();
```
这个很简单，因为A是作为一个构造函数来使用的，所以这时的this指向的是a

```
var A = function(){
	console.log(this);
}
A();
```
这里A是作为一个普通函数被调用的，当函数被作为一个普通函数调用时this指向全局变量，即使在嵌套了很多层的复杂情况也是如此。

然后再看一个情况:

```
var a = {
	func:function(){
		console.log(this);
	}
}
a.func();
```
这里func是作为一个对象a的成员方法被调用的，所以this指向的是对象a本身。

我们不考虑通过bind和apply设定this的情况，则不论代码多么复杂，最终都可以归结为上面的三种情况，然后分析属于哪种就行了。

比如写个复杂点的例子

```
var A = function(){
	console.log(this);	//1
	var B = (function(){
		console.log(this);	//2
		return function(){
			console.log(this);	//3
		}
	})();
	this.cb = function(){
		console.log(this);	//4
		B();	//43
	}
	B();	//53
}

var a = new A();
a.cb();
```
这里1很简单，this就是a，因为A作为一个构造函数。 2这里是在一个闭包里，这个立即执行函数是被直接调用的，所以这里的this也是global。3这里会被执行两次，分别为43和53，但这两种情况都是直接执行函数，所以this也都是global。至于4，它被调用时是a.cb()的形式，cb作为a的成员函数被调用，所以this时a本身。

至于bind和apply，使用它们给一个函数绑定了什么对象，这个函数被调用时，this就是什么对象。举个简单的例子

```
var a = {
	func:function(){
		console.log(this);
	},
	func1:function(){
		console.log(this);
	}.bind(this)
}

a.func();		//1
a.func1();	//2
```
1这里this就是a本身，2这里则是global。2这里往func1绑定的this，是在定义a时环境的this，而不是a本身，需要注意，例如

```
var A = function(){
	var a = {
		func:function(){
			console.log(this);
		},
		func1:function(){
			console.log(this);
		}.bind(this)
	}

	a.func();		//1
	a.func1();	//2
}
var tmp = new A();
```
这时1的this仍然是a, 而2的this就是就是tmp
