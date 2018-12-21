---
title: ReactNative之红屏是如何产生的
date: 2018-12-11 19:15:36
tags: ReactNative
---
我们在开发RN项目时，红屏是司空见惯的事情，然后我发现很多人会问，调试时出现红屏，那应用发布后是否会红屏呢？要确定的知道答案，还得从源代码去看。

在node_modules/react-native/Libraries/Core/InitializeCore.js中有一段代码

    const handleError = (e, isFatal) => {
      try {
        ExceptionsManager.handleException(e, isFatal);
      } catch (ee) {
        console.log('Failed to print error: ', ee.message);
        throw e;
      }
    };
    const ErrorUtils = require('ErrorUtils');
    ErrorUtils.setGlobalHandler(handleError);
这是默认的异常处理函数。handleException的实现，在node_modules/react-native/Libraries/Core/ExceptionsManager.js中
    
    const {ExceptionsManager} = require('NativeModules');
    ExceptionsManager.reportFatalException
    ExceptionsManager.reportSoftException
然后就进入到了原生代码中。

先看iOS中的RCTExceptionManager.m中的reportFatalException函数可以看到

    [_bridge.redBox showErrorMessage:message withStack:stack];
    if (_delegate) {
      [_delegate handleFatalJSExceptionWithMessage:message stack:stack exceptionId:exceptionId];
    }
    static NSUInteger reloadRetries = 0;
    if (!RCT_DEBUG && reloadRetries < _maxReloadAttempts) {
      reloadRetries++;
      [_bridge reload];
    } else {
      NSString *description = [@"Unhandled JS Exception: " stringByAppendingString:message];
      NSDictionary *errorInfo = @{ NSLocalizedDescriptionKey: description, RCTJSStackTraceKey: stack };
      RCTFatal([NSError errorWithDomain:RCTErrorDomain code:0 userInfo:errorInfo]);
    }
这就是产生红屏的代码，可以看到，只要异常进入到原生层，都会出现红屏，不论是连本地webserver调试，还是加载包内或文件夹内bundle，更和打bundle时是否是dev模式无关。然后可以看到这里允许使用delegate在收到错误时进行额外处理，例如进行上报。如果是release模式且设置了maxReloadAttempts值（默认为0），就会进行reload重试，再进去RCTFatal函数可以看到它的实现是抛出了一个异常，但debug模式下会try catch住，避免应用崩溃，而release模式下则不会try catch，异常会继续抛出。

android端要复杂一些，首先仍然是找到ExceptionManagerModule.java，它里面的实现是

    if (mDevSupportManager.getDevSupportEnabled()) {
      mDevSupportManager.showNewJSError(title, details, exceptionId);
    } else {
      throw new JavascriptException(JSStackTrace.format(title, details));
    }
如果mDevSupportManager.getDevSupportEnabled返回true，那么就会调用showNewJSError处理，否则直接抛出异常，这会导致应用直接闪退。mDevSupportManager的来源是ReactInstanceManager的构造函数，通过源代码可以看到如果useDeveloperSupport为false,则使用的是DisabledDevSupportManager，否则是DevSupportManagerImpl。useDeveloperSupport又来自于ReactNativeHost的接口getUseDeveloperSupport，模板工程里它的实现是

    public boolean getUseDeveloperSupport() {
      return BuildConfig.DEBUG;
    }
所以对android端来说，release模式使用的DisabledDevSupportManager的getDevSupportEnabled返回false，所以在接到js层传来的异常时会直接抛出一个java异常，然后就结束了。debug模式使用的DevSupportManagerImpl，它的getDevSupportEnabled由ReactInstanceManager调用setDevSupportEnabled进行控制，它的showNewError就是产生红屏的具体实现代码。

根据上面的一路跟踪，我们可以得出的结论是：
1. 如果不想出现红屏，最方便的办法就是在js层使用ErrorUtils.setGlobalHandler捕获异常，这样异常不会被传到原生层，也就不会导致红屏了
2. 如果异常被传到原生层，iOS端一定会出现红屏，release模式下可能闪退。Android端在release模式下不会红屏但可能会闪退，debug模式下则会红屏