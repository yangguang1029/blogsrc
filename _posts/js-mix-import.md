---
title: js之import与export复合
date: 2017-12-15 16:33:43
tags: javascript
---
在重构项目时有时会有这种需求，从一个文件内import进来然后export出去。这里总结一下一些写法，在[ECMAScript6 入门](http://es6.ruanyifeng.com/#docs/module)里有一段相关内容可做参考。内容很简单，基本就是语法规范而已。

首先是导出文件a.js

	//a.js
	let a = {"a":1}
	export {a}
	
b.js需要导入a.js再导出，有一种比较简单的写法

	//b.js
	export {a} from "./a"
在使用的时候

	//index.js
	import {a} from "./b"
跟从b.js内正常export出来的一样对待。

还有一种写法效果一样，但有一点区别。就是

	//b.js
	import {a} from "./a"
	export {a}
这种写法的作用是**在b.js内可以使用变量a**，而前一种写法不能。

如果a.js导出的比较多，一般会使用import \* 来引用，也可以使用export \* 来导出，例如

	//b.js
	export * from './a'
	export let b = {"b":2}
	//index.js
	import * as B from "./b"
	console.log(B.a); 

然后看一下export default的情况

	//a.js
	export default a = {"a":1}
	//b.js
	export a from "./a"					//（1）

	export {default as a} from "./a"	//(2)

	import a from "./a"					//(3)
	export {a}
	//index.js
	import {a} from "./b"
第一种写法是错误的，第二种和第三种写法没问题，而且这两种写法在b.js内都可以正常使用变量a

也可以把一个普通的export转换为export default，例如

	//b.js
	export {a1 as default} from "./a"
	//index.js
	import a1 from "./b"
但这种方法在b.js内不能使用变量名a1，如果要使用的话，下面这样写就可以了

	//b.js
	import {a1} from "./a"
	export default a1