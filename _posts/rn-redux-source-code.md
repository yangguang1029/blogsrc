---
title: ReactNative之Redux源码阅读(createStore)
date: 2019-07-24 21:15:36
tags: ReactNative
---

很久没写点啥了，一来是最近半年事情很多，二来是自己也迷茫了挺长时间，现在有点缓过来，应该要恢复记点东西了。言归正传，前几天看到说redux源码总共只有600来行，很容易看懂，于是去看了一眼，发现确实是，大概用了两个小时就全部看完了，也确实很容易看明白，想到不少同学对redux有一种犯怵和抵触的心理，顿时觉得很没必要，不信也去看一看源码吧。

这个Redux源码阅读系列会把整个Redux的源码都过一遍，适合对redux已经有足够了解的同学，如果不是很了解，建议仔细把[官方文档](https://www.redux.org.cn/)再看一看。话不多说，进入Redux在github上的[仓库](https://github.com/reduxjs/redux/tree/master/src)，可以看到文件数量只有几个，我们一个一个的讲

### index.js

我们要看一个js库的源码，首当其冲就是[index.js](https://github.com/reduxjs/redux/blob/master/src/index.js)，这里展示了对外暴露的接口，我们可以看到熟悉的createStore, combineReducers, bindActionCreators以及applyMiddleware。这就过去一个文件了，有没有信心满满呢？哈哈

### createStore.js

然后是[createStore.js](https://github.com/reduxjs/redux/blob/master/src/createStore.js)，最顶上的注释把大部分的内容都介绍到了，先看完注释再看源码，会轻松很多。createStore顾名思义是用来创建store，redux的[三大原则](https://www.redux.org.cn/docs/introduction/ThreePrinciples.html)第一条是单一数据源，所以整个App只会创建一个store。

createStore接受的第一个参数是reducer函数，第二个是可选参数preloadState，第三个是可选参数enhancer。其中reducer函数不用多说，它可以是一个普通函数，或者使用combineReducer生成的函数。preloadState是state的初始值，如果需要设置初始state则传入这个参数，需要注意如果使用了combineReducers，那么preloadState和combineReducers的结构也就是keys需要一致。enhancer参数用来加强redux的能力，Redux自带的applyMiddleware就是一个enhancer。combineReducer和applyMiddleware后面都会看到它们的源码。

然后再看一下返回值，它返回的是一个object，内容是

    return {
        dispatch,
        subscribe,
        getState,
        replaceReducer,
        [$$observable]: observable
    }

我们直接看这4个返回的方法都做啥，createStore函数最开始那些参数的校验之类的可以快速跳过。

#### dispatch
先看dispatch方法，dispatch方法就是发出一个action，这个action会被reducer函数处理，生成新的state，然后通知所有注册了监听的组件。它接受一个参数action，action必须是一个plain object，而且必须有type值。

然后是一个开关变量isDispatching，在reducer函数还没执行完之前，是不允许又接收一个action来执行reducer函数的，所以使用这个变量来做开关。

接着currentState = currentReducer(currentState, action)就是调用reducer函数来得到新的state并赋值，之后可以看到遍历了所有的listeners。

#### subscribe

subscribe用来注册一个监听，前面dispatch修改了state之后，会通知所有的监听者，监听者就是通过subscribe来注册的。

这里的细节是维护了两个listeners队列：currentListeners和nextListeners，在dispatch方法里，先把nextListeners赋值给currentListeners，然后遍历currentListeners，然后在subscribe时，通过ensureCanMutateNextListeners函数拷贝一份currentListeners给nextListeners，然后修改nextListeners。虽然听起来有点绕，但并不难理解，在遍历listeners期间如果注册监听和取消监听，肯定不能修改正在遍历中的数组，所以需要维护两个，一个用来遍历，另一个用来修改。

subscribe函数返回一个unsubscribe函数，这也是js库里常见的一种设计，用来取消注册监听，代码非常好看懂。

#### observable

这里代码不是很好看懂，它用了一个第三方库[symbol-observable](https://github.com/zenparsing/es-observable)，但大概可以看明白这个函数做了什么，它对外暴露了一个subscribe接口，内部实际上是调用上面的subscribe进行注册监听，对外暴露的subscribe需要接受一个observer object。在react-redux中应该能看到这个接口的实际应用。

#### getState和replaceReducer

这两个比较简单，一起带过，前者是获取到state值。后者是整体替换掉reducer，实际中用到的不多。

#### dispatch({ type: ActionTypes.INIT })

createStore函数在return之前，dispatch了这么一个action，reducer函数可以用这个action来做初始化工作，当然我们一般都是在reducer函数中用默认值来做初始化，所以这个action实际中很少会用到，但了解这个细节其实会很有用的。

#### 结语

写到后面发现如果把所有源码阅读写成一篇会太长了，所以就做成系列吧，接下来再陆续把剩下的写完。顺便感慨一下，读完源码加记完笔记用了俩小时，现在写这一篇就用了俩小时差不多，还写的很不咋的，语言和文字表达能力有点太堪忧，总是前言不搭后语，可见要写一篇好博客，真的很不容易啊……