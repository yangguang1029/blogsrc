---
title: ES6之Promise
date: 2017-04-06 20:14:39
tags: javascript
---
Promise是对异步操作做的封装，它解决的是回调嵌套的问题，它的实现仍然是注册和调用回调函数。

### 构造和使用
使用Promise很简单，例如

```
var p = new Promise(function(resolve, reject){
	//do some asynchronous thing
	if(xxx) {
		console.log("resolve ...")
		resolve();
	}else{
		console.log("reject....")
		reject();
	}
})
p.then(function(){
		console.log("in resolve callback");
	}, function(){
		console.log("in reject callback");
	}
)
```

在构造时，传入一个函数作为参数，在这个函数里做我们需要做的事情，比如某个异步操作，然后在恰当的时候，调用resolve或者reject。

一个Promise对象有三种状态，pending（进行中）, resolved（已解决）, rejected（已失败），初始是pending状态,当resolve或者reject函数被调用时进入resolved或者rejected状态，我们通过then方法，分别指定resolved和rejected的回调，当状态变化时，相应的回调就会被调用。

需要注意的是Promise对象在创建时传入的函数，会立即执行，但它的回调，则在当前脚本所有同步任务都执行完成后，才会开始执行。所以对于下面的代码，输出是132，而不是123

```
var p = new Promise((resolve, reject)=>{
	console.log("1");	
	resolve()
})
p.then(()=>{
	console.log("2");
})
console.log("3");
```

### Promise.resolve, Promise.reject

这两个是Promise类的静态方法，通过它可以生成一个Promise对象，它的状态已经是resolved或者rejected，实际上下面这两种方式是等同的

```
var p = Promise.resolve(123);
var p = new Promise(function(resolve, reject){
	resolve(123);
})
```

这两个方法还可以接受thenable对象，将其转换成Promise对象,一个thenable对象就是具有then方法的对象，例如

```
class Test {
	then(resolve, reject) {
		if (resolve) {
			resolve();
		}
		if (reject) {
			reject();
		}
	}
}

let t = new Test();
t.then(() => {
	console.log("resolved....");
})
let p = Promise.resolve(t);
```

### promise chain
then函数返回的是一个新的Promise对象，而不是我们在resolve或者reject回调里return的值，所以我们可以在then函数后面继续接then函数，形成一个promise链，例如

```
var p = Promise.resolve(1);
p.then((v1)=>{
	console.log("resolve 1...."+v1);
	//throw new Error();
	//return Promise.reject();
	//return Promise.resolve();
	/*
	return new Promise(function(resolve, reject){
		setTimeout(()=>{
			resolve();
		}, 5000)
	})
	*/
	return 2*v1;
}).then((v2)=>{
	console.log("resolve2...." + v2)
}, (reason)=>{
	console.log("reject2...")
})
```

如果我们在then的回调函数里return了一个pending状态的Promise对象，则等待这个对象状态变化后进入下一个then的相应回调中。如果返回一个rejected状态的Promise对象，或者抛出了一个错误，那么会立刻进入下一个then的reject回调中，否则立刻进入下一个then的resolve回调中。如果return的不是Promise对象，则return的值会作为下个then里回调的参数值。

### promise对象作为resolve或者reject参数
当我们调用一个Promise对象a的resolve函数时，如果参数是另一个promise对象b，那么只有当b的状态发生改变，a的状态才会改变。且a的状态取决于b的状态

当我们调用一个Promise对象a的reject函数时，如果参数是另一个promise对象b，则a的状态不需等待b的状态，且a的状态不受b影响，一定是rejected。以下是实验代码

```
let p1 = new Promise(function(resolve, reject) {
		setTimeout(() => {
			// console.log("resolve p1....");
			// resolve();
			console.log("reject p1....");
			reject();
		}, 5000)
	})

let p2 = new Promise(function(resolve, reject) {
		setTimeout(() => {
			// console.log("resolve p2...");
			// resolve(p1);
			console.log("reject p2....");
			reject(p1);
		}, 1000)
	})

p2.then(function(value) {
		console.log("in p2 resolve callback");
	}, function(error) {
		console.log("in p2 reject callback");
	});

p1.then(function(value) {
		console.log("in p1 resolve callback");
	}, function(error) {
		console.log("in p1 reject callback");
	});
```

输出为

```
resolve(p1), p1 resolve

resolve p2...
resolve p1...	//4秒后
in p1 resolve callback
in p2 resolve callback
/**************************************/
resolve(p1), p1 reject

resolve p2...
reject p1...	//4秒后
in p1 reject callback
in p2 reject callback
/**************************************/
reject(p1), p1 resolve

reject p2...
in p2 reject callback
resolve p1	// 4秒后
in p1 resolve callback
/**************************************/
reject(p1), p1 reject

reject p2...
in p2 reject callback
reject p1	//4秒后
in p1 reject callback

```

### Promise.all Promise.race

它们都接收一个Promise数组作为参数，并返回一个新的Promise。

对于all来说，只有当数组里每个Promise对象状态都变成resolved，新对象的状态才变成resolved，它在then的resolve回调函数参数为一个数组，包含所有Promise的返回值。但只要有一个Promise对象状态变为rejected，那么新对象的状态马上变为rejected。此时reject的参数被传递给then的reject回调

对于race，只要有一个Promise对象状态发生了变化，新对象的状态就马上跟着改变。第一个改变状态的对象的返回值作为新对象回调的参数。