---
title: googleClosureCompiler使用
date: 2016-08-15 20:47:56
tags: google-closure-compiler
---
官方文档[在此](https://developers.google.com/closure/compiler/)

最简单的使用命令如下

```
java -jar compiler.jar --js hello.js --js_output_file hello-compiled.js
```

使用

```
java -jar compiler.jar -help
```

可以显示帮助，通过它可以查询有哪些可配置参数，及它们的可选值，默认值

这里再介绍一下其他的一些常用参数，像–charset这种不是很常用到的参数就不一一举例了，用help查看即可，需要注意的是，随着compiler.jar的版本不一样，可选参数以及默认参数也可能会不一样，以help给出的文档为准即可

- –js指定输入文件名
- –js_output_file 指定输出文件名，如果不设置此参数，则默认输出到stdout
- –compilation_level 混淆级别，可选参数WHITESPACE_ONLY，SIMPLE_OPTIMIZATIONS，ADVANCED_OPTIMIZATIONS。默认值为SIMPLE_OPTIMIZATIONS。WHITESPACE_ONLY只会移除掉空格和注释，SIMPLE_OPTIMIZATIONS会简化局部变量名，ADVANCED_OPTIMIZATIONS通常称为深度混淆，他简化局部以及全局变量名，移除deadCode，并且对一些函数inlining。
- –externs 在使用深度混淆时，如果不希望一些变量名被混淆，则需要使用此参数。可以指定多个extern参数，但每个参数都需要使用一次–externs
- –language_in 可选值包括ECMASCRIPT3,ECMASCRIPT5,ECMASCRIPT5_STRICT，默认值是ECMASCRIPT3，所以如果需要混淆的代码中包含ECMASCRIPT5特性，则必须指定此参数，ECMASCRIPT5_STRICT会使用[严格模式](http://www.ruanyifeng.com/blog/2013/01/javascript_strict_mode.html)

使用SIMPLE_OPTIMIZATIONS没什么好说的，主要是使用ADVANCED_OPTIMIZATIONS时需要注意一些，避免被坑，建议详细阅读下[官方文档](https://developers.google.com/closure/compiler/docs/api-tutorial3)

简单而言：

1. 为了避免未调用方法被移除，可以进行一次调用，或者export出来
1. 对成员属性调用的方式有.key和[“key”]两种，因为字符串不会被混淆，所以对于不希望被混淆的变量名，应该采取第二种方式。而且对同一个成员属性，不应该两种方式混用，否则有的地方呗混淆，有的地方被保留，就肯定出错了。这里有个小细节，第一次赋值时使用.key的方式，key不会被混淆。
1. 因为深度混淆会简化全局变量名，所以必须将需要混淆的所有代码统一进行混淆，否则定义时的变量名被混淆成了a，使用时混淆为b
1. 混淆和未混淆代码的相互调用。这其中还包括一种隐藏的形式eval，因为eval内的代码是字符串形式所以不会被混淆。未混淆代码调用混淆代码，解决方案为混淆代码使用字符串为key的方式将接口导出。混淆代码调用未混淆代码，解决方案是使用extern参数