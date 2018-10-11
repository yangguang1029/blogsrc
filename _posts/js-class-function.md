---
title: javaScript之类的成员函数和箭头函数
date: 2018-08-29 11:44:45
tags: javascript
---
最近发现有的地方在使用ES6的class时，使用箭头函数来声明方法，例如

```
class Test {
  func1(num){
    this.num = num
  }
  func2 = (num) => {
    this.num = num
  }
}
var t = new Test()
```
这两种方案是有区别的，区别就是func1是protoType上的属性，而func2是实例上的属性，我们用console.dir(t)在chrome dev tool上一看就知道了。根据prototype的原理，func1对于所有的实例只有一份，func2对每个实例都有一份。

所以对于需要bind的函数，例如要用在闭包里，那使用箭头函数或者bind没有区别，bind也会生成一个新的函数对象赋给this。但如果是不需要bind的函数，写成箭头函数就会造成内存浪费了，应该避免。

对于属性property，在constructor内声明还是在类中声明则没有区别，两者都是实例属性。
