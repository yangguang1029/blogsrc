---
title: ES6中循环引用的坑
date: 2017-11-13 20:08:14
tags: javascript
---
今天碰到一个很诡异的问题，在import一个模块后直接使用，结果就报红屏错误 undefined is not a function，当时很奇怪，明明那个模块export了很多东西，而且别的地方import又是正常的，为什么在这里import就出问题呢？用console打印出来，发现import进来的结果是个{}。代码大概就是
	
	import Test from "./test"
	Test.test();	//这里报错，说test是个undefined，所以不能当做方法调用
后来突然想到，可能是产生循环引用了，一查果然是这个原因。因为项目比较庞大，不小心还是很容易间接产生循环import。

查阅[阮老师的ES6教程](http://es6.ruanyifeng.com/#docs/module-loader)里有ES6关于循环import的说明。写一个简单的例子

	//a.js
	console.log("before import b")
	import {b} from "./b"
	console.log("b is " + b)
	export let a = b+1;
	
	//b.js
	console.log("before import a")
	import {a} from "./a"
	console.log("a is " + a)
	export let b = a+1;
结果是
	
	before import a
	a is undefined
	before import b
	b is NAN
这里有一个有趣的现象就是第一句输出并不是before import b，也就是虽然import语句在后面，但确会更早执行，当执行import b时，加载并运行b.js，从而第一句输出是before import a。

然后就是当运行b.js时，发现又需要import a.js，此时不会再去加载a.js了，而是认为整个a.js模块是{}，所以a的值就是undefined了。可以通过以下代码验证
	
	//b.js
	import * as A from "./a"
	console.dir(A)	//输出为{}
因为循环import一旦出现查找起来比较麻烦，经过了好多个中转，每个文件又都import了很多，很难找到是怎么导致循环的。一个避免出问题的方法就是少写立即执行的代码，尽量使用函数封装起来，需要的时候调用函数，就不会出错了。

对于像constants, enum, global等一些需要立即执行的模块，则手动确保不要产生循环即可。