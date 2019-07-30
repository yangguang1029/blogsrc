---
title: ReactNative之Redux源码阅读(applyMiddleware,compose)
date: 2019-07-29 21:15:36
tags: ReactNative
---

去掉utils目录和compose这些辅助类，applyMiddleware是最后一个暴露的接口源码了，果然redux代码还是很好看懂的。当然这主要是因为代码质量很高，而且注释很完善，这是我们自己写sdk时值得学习的榜样，接下来就看下applyMiddleware的代码。

### applyMiddleware

在[ReactNative之Redux源码阅读(createStore)](http://yangguang1029.github.io/2019/07/24/rn-redux-source-code/)里提到了enhancer函数，applyMiddleware就是redux内置的一个enhancer。enhencer函数都接受createStore函数作为参数，然后返回新的createStore函数。

老样子，先看一下代码注释，然后看具体的代码实现，applyMiddleware接受的参数是middlewares数组，在它返回的createStore函数里，先调用createStore得到store，然后拿middlewares加工store.dispatch方法，最后返回store和加工后的dispatch函数。

    const middlewareAPI = {
      getState: store.getState,
      dispatch: (...args) => dispatch(...args)
    }
    const chain = middlewares.map(middleware => middleware(middlewareAPI))
    dispatch = compose(...chain)(store.dispatch)

从这里可以看到，每个middleware函数接受middlewareAPI参数，其中包含getState和dispatch两个属性，并返回一个函数，返回的函数通过compose组合起来（详见[compose.js](https://github.com/reduxjs/redux/blob/master/src/compose.js)内的代码注释），所以这个返回函数接受的参数是上一个middleware函数的返回值(也是dispatch函数)，并返回dispatch函数（会成为下一个middleware的参数）。也就是middleware函数的定义是

    function myMiddleware({getState, dispatch}) {
        return function(next) {
            return function(action) {
                return next(action);
            }
        }
    }
    // 箭头函数写法
    const myMiddleware = ({getState, dispatch}) => next => action => next(action)

建议看一下[redux-thunk的代码实现](https://github.com/reduxjs/redux-thunk/blob/master/src/index.js)加深一下理解。

整个redux的源码到这里就结束了，到这里就会发现真的没太多内容，接下来再看一下React-redux的代码，因为一般redux都会配合React-redux来使用，而且它的代码也不复杂。