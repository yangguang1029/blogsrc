---
title: c++11之lambda简单使用
date: 2017-03-10 17:28:10
tags: c++
---

lambda是C++11新增的功能，因为不是很熟，碰到需要回调的时候，我都是使用std::bind来绑定函数指针，但lambda有它使用方便的地方，尤其是闭包可以调用函数内的局部变量的特性，非常灵活，所以用简单的笔记记录下怎么使用，详细可以参考[官方文档](http://zh.cppreference.com/w/cpp/language/lambda)

### 语法

```
[ capture-list ] ( params ) mutable(可选) constexpr(可选)(C++17) exception attribute -> ret { body }
[ capture-list ] ( params ) -> ret { body }
[ capture-list ] ( params ) { body }
[ capture-list ] { body }
```
1. mutable的作用是允许body修改按复制捕获的参数，及调用其非const成员函数，但修改只在lambda内起作用，不会真正改变外面的值。
2. 可以省略-> ret指定返回值类型，返回类型为void。但有一个例外，若body只由单条带表达式return语句组成，而不含其它内容，则返回类型是被返回表达式的类型（在左值到右值、数组到指针，或函数到指针隐式转换后）
3. 省略参数列表，等同于参数列表为()
4. 参数列表和普通函数的写法一样，但C++14之前不允许使用默认参数和auto类型。
5. 若隐式或显式地以引用捕获一个实体，且在该实体的生存期结束后调用闭包对象的函数调用运算符，则发生未定义行为。C++闭包不会延长被捕获引用的生存期。同样的规则应用于被捕获的this指针所指向对象的生存期
6. lambda表达式是一个纯右值表达式，它可以被赋值给std::function类型的变量

### 捕获列表规则

- [a,&b] 其中a以值捕获而b以引用捕获。
- [this] 以值捕获this指针
- [&] 以引用捕获所有lambda体内的odr使用的自动变量，及以引用捕获当前对象(*this)，若它存在
- [=] 以值捕获所有lambda体内的odr使用的自动变量，及以引用捕获当前对象(*this)，若它存在
- [] 无捕获

随便写个简单的例子：

```
std::for_each(arr.begin(), arr.end(), [](int item){
        cout << item << endl;
    });
std::find_if(arr.begin(), arr.end(), [](int item){
        return item %2 == 0;
    });
```