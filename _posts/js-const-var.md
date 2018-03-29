---
title: javaScript之let和var在闭包内的区别
date: 2018-03-07 10:45:21
tags: javascript
---
今天在解决一个bug时碰到的问题，经过层层抽象后，最终通过demo来测试，代码如下

    var functions = [];
    let str = `
        var a = [1,2,3];
        functions.push(()=>{
            console.log(JSON.stringify(a))
        })
    `;
    eval(str);
    let str1 = `
        var a = [4,5,6];
        functions.push(()=>{
            console.log(JSON.stringify(a))
        })
    `;
    eval(str1);

    for(var func of functions){
        func();
    }
因为原来碰到的问题是加载两个不同的bundle，所以对应的只能通过两次eval来模拟了。对于上面的代码，我预测的结果是输出两个[4,5,6]数组，因为第二次eval的时候，a被赋予了新值，当闭包执行时，它通过对外部变量a的引用，获取的是a的最新值，实际上的输出也确实是如此。但如果这样的话，就不应该产生bug才对，左思右想之下，突然发现源代码里不是var a，而是const a。于是赶紧改成const试一下，这次输出就是[1,2,3]和[4,5,6]了，const和let是一样的，换成let试一下，也是输出[1,2,3]和[4,5,6]

通过这个表现，很容易推测到什么原理。在js中，是不允许对同一个变量名使用两次let的，但显然通过eval不受这个限制。当使用var时，两次eval执行后，仍然只有一个变量a。但当使用let和const时，再次eval，虽然变量名一样，但实际上不是同一个变量了，否则就会运行报错了，既然不是同一个变量，那么理所当然两个闭包持有的是各自对应的那个外部变量，所以就产生了不同的结果。

我们在实际项目中虽然尽量避免使用eval，但解释器多次加载和执行代码是经常出现的，此时就要小心这种情况了。
