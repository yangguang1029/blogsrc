---
title: ES6之Promise
date: 2017-04-06 20:14:39
tags: javascript
---
Promise本质上是对异步操作做的封装。

### 构造
构造一个Promise，我们需要传入一个function作为参数。在这个function里我们开始做异步的操作，例如网络通信或者定时。例如

```
var p = new Promise(function(resolve, reject){
	//do some asynchronous thing
})
```
这里resolve和reject


```
function test1(){
	let p1 = new Promise(function(resolve, reject){
		setTimeout(()=>{
			console.log("resolve p1....");
			resolve("p1 resolve");
		}, 5000)
	})

	let p2 = new Promise(function(resolve, reject){
		setTimeout(()=>{
			console.log("resolve p2...");
			resolve(p1);
		}, 1000)
	})

	p2.then(function(value){
		console.log("in p2 resolve callback");
	}, function(error){
		console.log("in p2 reject callback");
	});

	p1.then(function(value){
		console.log("in p1 resolve callback");
	}, function(error){
		console.log("in p1 reject callback");
	});
}

```

1. resolve(p1), p1 resolve
```
resolve p2...
resolve p1...	//4秒后
in p1 resolve callback
in p2 resolve callback
```
2. resolve(p1), p1 reject
```
resolve p2...
reject p1...	//4秒后
in p1 reject callback
in p2 reject callback
```
3. reject(p1), p1 resolve
```
reject p2...
in p2 reject callback
resolve p1	// 4秒后
in p1 resolve callback
```
4. reject(p1), p1 reject
```
reject p2...
in p2 reject callback
reject p1	//4秒后
in p1 reject callback
```
