---
title: JavaScript之unhandled promise rejection
date: 2019-09-25 20:44:45
tags: javascript
---

在JavaScript中，unhandled promise rejection问题有两种场景，一个是promise没有写catch，但是又变成了rejected状态，另一种是promise写了catch，但是catch中又抛出了异常，例如：

````
// 场景一
Promise.reject().then()
// 场景二
Promise.reject().catch(err => {
  throw new Error()
})
````

在[这篇文档](https://javascript.info/promise-error-handling#unhandled-rejections)里提到：如果在promise内发生异常，而这个promise又没有catch，那么这个promise会变成rejected状态，然后系统会抛出一个全局异常，原文是

> JavaScript engine tracks such rejections and generates a global error

但经过google和实际观察，我发现这并不准确。这篇文章里一直在拿“普通异常未做catch”和“unhandled promise rejection”做类比，但我感觉这二者其实没很多共通的地方，也许作者只是为了便于读者理解吧。

那么实际上会发生什么呢？目前来看，发生unhandled promise rejection不会抛出异常，也就不会导致JavaScript运行中断（写个demo验证下就知道了）。在浏览器中，我们可以在控制台看到有个红色的Uncaught (in promise)报错，同时系统会抛出一个unhandledrejection事件，我们使用window.addEventListener来监听到，例如

````
window.addEventListener('unhandledrejection', function(event) {
  // the event object has two special properties:
  console.log(event.promise); // [object Promise] - the promise that generated the error
  console.log(event.reason); // Error: Whoops! - the unhandled error object
});
````
在nodejs环境中，可以看到一个UnhandledPromiseRejectionWarning警告，同时系统也会抛出一个unhandledRejection事件，使用process.on('unhandledRejection'）来统一监听。在未来的版本中可能会抛出异常，总之完全取决于JavaScript解释器如何处理。

我们在实际代码中，显然不能依赖于监听unhandledrejection事件来统一处理的方式，更靠谱的办法是养成好的编码习惯，首先是使用promise时都配备catch函数，即使给个空函数都可以，其次是在最终的catch函数里，最好使用try-catch包装，避免继续抛出异常。当然，使用监听unhandledrejection来做兜底方案也是很有必要的。