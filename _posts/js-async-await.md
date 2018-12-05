---
title: javaScript之简单理解async函数
date: 2018-12-04 20:50:39
tags: javascript
---
async函数和generator函数这个东西，如果用到的不多，很容易看着犯怵，尤其是还搭配上promise，我自己就是这样，几个月前觉得明白这些概念，但因为用的不多，几个月后感觉又稀里糊涂了，所以尝试用最简单的方式来解释。

首先是generator函数，它的函数声明比普通函数多了个星号，然后函数内容可以使用yield关键字

    function* generatorFunc() {
      console.log(0)
      yield 1
      console.log(1)
      yield 2
      console.log(2)
      yield 3
      console.log(3)
    }
执行generator函数会返回一个遍历器对象，使用它可以控制函数的执行，例如

    let iter = generatorFunc()
    let result = iter.next()
    while(!result.done) {
      result = iter.next()
    }
每次调用next，就会执行到下一个yield，直到函数结束，这是最简单的介绍，想了解更多的话请参考[阮老师的ES6教程](http://es6.ruanyifeng.com/#docs/generator)

然后是async-await，它就是generator函数的语法糖，async相当于函数声明中的星号，await相当于yield，除此之外，async函数在执行后不是返回遍历器，而是自动执行完。例如

    async function asyncFunc() {
      console.log(0)
      await 1
      console.log(1)
      await 2
      console.log(2)
      await 3
      console.log(3)
    }
    let p = asyncFunc() // p是一个promise对象
这个函数一执行，就会立即输出0123，函数返回的是一个Promise对象，当我们在函数里return时，就会进入到这个promise的then回调，如果函数内抛出异常，就会进入到它的catch回调中。

到上面为止，我们只看到async函数比generator函数用起来方便些，还看不出来它们的真正用途，所以我们把await后面的数字换成promise对象，先用一个promise来模拟一下异步操作

    function getPromise() {
      return new Promise((resolve, reject) => {
        setTimeout(()=>{
          let random = Math.floor(Math.random() * 100)
          if(random > 20) {
            resolve(random)
          }else {
            reject(random)
          }
        }, 1000)
      })
    }
这个函数很好理解，生成一个延迟1秒的promise，80%的几率resolve, 20%的几率reject，然后我们在async函数里使用它

    async function asyncFunc() {
      let result = await getPromise()
      console.log(result)
      result = await getPromise()
      console.log(result)
      result = await getPromise()
      console.log(result)
    }

执行这个函数

    asyncFunc().then(result=>{
      console.log('result ' + result)
    }).catch(error=>{
      console.log('error ' + result)
    })
很容易理解，当await后面是一个promise时，会等待这个promise执行完，如果结果是resolve，值就会被返回给result，如果是reject，就会中断函数的执行，进入到返回promise的catch中。

通常在async函数中，我们需要用try-catch来处理promise的reject情形，例如

    async function asyncFunc() {
      try{
        let result =  await getPromise()
        console.log(result)
      }catch(error) {
        console.log('error ' + error)
      }
    }
这样我们就不用再对这个函数返回的promise来写then和catch了。如果不喜欢写try-catch，可以考虑做一些封装来改变形式，例如[how-to-write-async-await-without-try-catch-blocks-in-javascript](https://blog.grossman.io/how-to-write-async-await-without-try-catch-blocks-in-javascript/)

我们可以这样理解，await后面的参数其实都是promise对象，最开始例子中的await 1，其实是await了一个立即执行的promise对象。

最后是看一下redux-saga内的generator函数，因为我自己就是从这里开始糊涂的，如果对redux-saga不了解就请直接忽略。在redux-saga内，我们通常是这么写

    export default function* rootSaga(){
      yield all([
        takeEvery(ActionTypes.SAGA1, helloSaga),
      ])
    }

    function* helloSaga(){
      console.log('helloSaga start')
      try{
        yield g()
        let a = yield p()
        console.log('helloSaga ' + a)
      }catch(e) {
        console.log('error ' + e)
      }
    }

    function *g() {
      console.log('g start')
      let a = yield p()
      console.log(' g a ' + a)
      a = yield p()
      console.log(' g a ' + a)
    }
上面的代码在redux-saga环境下是可以运行的好好的，但如果不在redux-saga环境里，就别想它运行了，例如

    let a = helloSaga()
    a.next()
这里就输出'helloSaga start'就没了，因为g()返回的是一个遍历器，这个遍历器并没有执行，除非我们把helloSaga内改成

    let iter = g()
    iter.next()
    iter.next()
才能执行起g函数，然而此时g函数内输出的a都是undefined，而不像redux-saga环境内能够输出数字，这是因为yield的返回值，实际上是遍历器调用next时输入的值，具体可以去参考阮老师的ES6教程相关章节。

上面这段啰里啰嗦，总结起来就是：redux-saga内部帮我们做了封装，所以在yield后面接一个promise，返回值是resolve的值，也可以接一个generator函数或者async函数，这个函数会被执行，且函数内yield promise也会返回其resolve值，但不要误以为generator函数就是可以这么用的，如果不在redux-saga环境中，这样写不会达到想要的效果，至于redux-saga内是怎么封装的，相信对generator函数充分理解后肯定能明白的。

