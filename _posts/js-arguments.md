---
title: javaScript中的arguments
date: 2017-02-18 11:44:45
tags: javascript
---
### arguments
js中的每一个函数，都有一个默认的局部变量arguments，通过它可以获取到传给函数的所有实参，直接用序号获取即可，例如

```
function test(){
	console.log(arguments.length);	//2
	console.log(arguments[0]);	//1
	console.log(arguments[1]);	//haha
	console.log(arguments[2]);	//undefined
}
test(1, "haha");
```
虽然它有length属性和通过下标获取，但它并不是数组，它没有数组的其他属性和方法。如果想把它转成Array来使用，可以使用以下方法

```
var args = Array.prototype.slice.call(arguments);
var args = [].slice.call(arguments);
var args = Array.from(arguments); (ES2015)
var args = [...arguments]; (ES2015)
```
一般我们在定义一个函数时，会设定参数的数量，但它可能与实际传入的参数数量不一致，在上面这个例子里，前者可以通过test.length获取到，后者则是arguments.length。 所以使用arguments的主要目的就是在不确定实际传入的参数数量的时候。

### arguments与实参

arguments元素的值和实际参数的值，在没有[rest parameters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/rest_parameters), [default parameters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Default_parameters) 和[destructured parameters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)时，是会相互影响的

```
function test(a, b) {
	console.log("a is " + a);	// a is 1;
	arguments[0] = 10;
	console.log("a is " + a);	// a is 10;
	
	console.log("arguments[1] is " + arguments[1])	//arguments[1] is 2
	b=10;
	console.log("arguments[1] is " + arguments[1])	//arguments[1] is 10
}
test(1, 2);

```
否则就不会影响，上面例子改成 test(a, b, c=100) ,因为有了个参数c是default parameter，就导致arguments和实参互相不影响，结果就是显示

```
a is 1
a is 1
arguments[1] is 2
arguments[1] is 2
```

### arguments.callee
callee是arguments的一个属性，它指向当前执行的函数。如果在一个没有函数名的闭包函数里，使用它可以实现递归，例如

```
[1, 2, 3, 4, 5].map(function(n) {
    return !(n > 1) ? 1 : arguments.callee(n - 1) * n;
});
```
但是在ES5的严格模式里，是禁止使用callee的，而现在的很多主流浏览器，都实施了部分严格模式，所以要避免使用。

arguments.caller属性已经被废弃，不被支持了，可以使用Function.caller来代替，它指向调用当前函数的函数，如果值为null，则说明是global调用的。它虽然能被主流浏览器支持，但并没有进入标准，所以用的时候也要小心。以下是使用它实现记录当前调用栈

```
function stackTrace(){
	var f = stackTrace.caller;
	var s = "stack Trace:\n";
	while(f) {
		s += f.name;
		s += "\n";
		f = f.caller;
	}
	return s;
}
```