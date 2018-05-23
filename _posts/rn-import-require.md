---
title: ReactNative之两种模块管理方式
date: 2018-04-04 20:18:36
tags: ReactNative
---
在RN项目的js代码中，是可以使用两种模块管理方式的，分别是ES6风格和CommonJS风格，代码示例如

    //ES6风格
    //a.js
    export let a = 1;
    export function adda(){
        a += 1;
    }
    //index.js
    import {a, adda} from "./a.js"
    console.log("a is " + a)
    adda();
    console.log("after add a is " + a)
    
    //CommonJS风格
    //b.js
    let b = 1;
    function addb(){
        b += 1;
    }
    module.exports = {b, addb}
    //index.js
    let B = require("./b.js");
    console.log("b is " + B.b)
    B.addb();
    console.log("after add b is " + B.b)

这两者模块管理风格有什么区别，在阮一峰老师的《ECMAScript6 入门》书中，有[相关的章节](http://es6.ruanyifeng.com/#docs/module-loader)。例如ES6是静态导入，所以import必须位于顶层代码，任何位于非顶层代码的import都会报错，而require则可以位于任何位置。ES6风格因为是静态导入，import时模块名不能是动态的，而require可以是动态的。在导出时，ES6的导出是引用，而CommonJS的导出是拷贝，所以上面代码里，a会输出1和2，而b会输出两个1。

回到项目中来，我们在RN项目中的js代码，都会经过babel编译成ES5标准，在ES5中是没有模块管理的，所以RN自己实现了模块管理的功能，

先看导入，相关的源代码位于node_modules/metro/src/lib/polyfills/require.js内。我们在代码里不论是写import还是写require，最终都会被翻译成这个require.js里的require方法。通过这个方法可以看到，不论我们执行多少次导入，模块本身只会被加载执行一次。对同一个模块，我们使用ES6和CommonJS两种方式来引用，得到的行为是一样的。对上面的a.js，结果都是1和2，对b.js，结果都是两个1。然后不论使用哪种风格，文件之间的依赖顺序在编译成bundle时都必须确定下来，使用require因为可以写在代码块里，不像import必须写在顶层代码中，所以一定程度上可以延迟模块被执行的时间，个人觉得这个区别还是很微小的，不会造成性能上的区别。

然后是导出，前面说过这两种风格的导出结果，一个是拷贝，一个是引用。对上面的a.js和b.js，我们看一下他们在bundle内的代码就明白了

    __d(function (global, _require, module, exports, _dependencyMap) {
        Object.defineProperty(exports, "__esModule", {
            value: true
        });
        exports.adda = adda;
        var a = exports.a = 1;
        function adda() {
            exports.a = a += 1;
        }
    },337,[],"js/testImport/a.js");
    __d(function (global, _require, module, exports, _dependencyMap) {
        var b = 1;
        function addb() {
            b += 1;
        }
        module.exports = {
            b: b,
            addb: addb
        };
    },338,[],"js/testImport/b.js");
对于ES6风格的a.js，导出的属性直接加在了exports上，这个exports就是我们导入时获得的Object，所以它是直接持有了变量的引用。而对于CommonJS风格的b.js，导出的是一个新建的Object，它拷贝了变量b的值，既然是拷贝，就有浅拷贝和深拷贝之分，这里也完全取决于我们怎么实现，会有不同的行为，例如可以跑一下下面的代码试一下

    //b.js
    let b = {value:1}
    function addb(){
        b.value += 1;
    }
    module.exports = {b1:b, addb, b2:{value:b.value}}
    //index.js
    let B = require("./b.js");
    console.log("b1 is " + B.b1.value)
    console.log("b2 is " + B.b2.value)
    B.addb();
    console.log("after add b1 is " + B.b1.value)
    console.log("after add b2 is " + B.b2.value)

到这里基本上都明白了代码里的import, require, export, module.exports都有什么行为了。需要注意一下的就是，当import和require混合使用时，import一定会早于require被执行，这可能导致依赖顺序上发生问题，所以还是尽量避免混用。
