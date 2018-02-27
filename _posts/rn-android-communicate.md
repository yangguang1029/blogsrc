---
title: ReactNative之js与native通信流程（Android篇）
date: 2018-02-26 20:18:36
tags: ReactNative
---
这篇文章简要介绍一下android平台，js和java互相调用时，经过的流程。

### js调用java
要从js端调用java代码，需要把java端能被调用的接口，在js代码中进行注册。这个实现在react-native/Libraries/BatchedBridge/NativeModules.js文件中。

看NativeModules.js内的代码里有：

    let NativeModules : {[moduleName: string]: Object} = {};
    if (global.nativeModuleProxy) {
        NativeModules = global.nativeModuleProxy;
    } else {
        const info = genModule(config, moduleID);
        NativeModules[info.name] = info.module;
    }
这里把代码简化了一下，这段代码其实是说明了两种情况，当加载离线bundle时，genModule是从ReactCommon/cxxreact/JSCNativeModules.cpp里调进来的，否则是从ReactAndroid/src/main/jni/react/jni/ProxyExecutor.cpp里把__fbBatchedBridgeConfig传进来然后解析的。具体的细节不用深究。总之java端有哪些接口可供调用，模块名函数名等信息传到js层，然后经过一层封装，实际调用了MessageQueue里的enqueueNativeCall方法。

在enqueueNativeCall方法里我们可以看到一个细节，就是js对原生的调用是被存储在队列里的，每5毫秒把这些请求集中交给原生处理并清空一次队列。从js开始进入原生代码的入口是

    global.nativeFlushQueueImmediate(queue);
这个方法定义在ReactCommon/cxxreact/JSCExecutor.cpp中。它的实现是

    m_delegate->callNativeModules(*this, folly::parseJson(queueStr), false);
这个m_delegate如果一路跟踪的话，就会发现是一个JsToNativeBridge类实例，这个类定义在ReactCommon/cxxreact/NativeToJsBridge.cpp中。JsToNativeBridge的callNativeModules方法实现为

    m_registry->callNativeMethod(call.moduleId, call.methodId, std::move(call.arguments), call.callId);
进入ModuleRegistry类的callNativeMethod方法中，发现执行的是NativeModule类的invoke方法，而继承自NativeModule类的有两个：一个是ReactCommon/cxxreact/CxxNativeModule.h，我们用它实现了js与C++的直接通信，这个以后有空再写。另一个是ReactAndroid/src/main/jni/react/jni/JavaModuleWrapper.h里的JavaNativeModule。JavaNativeModule的invoke方法通过JNI调用了java方法。

    static auto invokeMethod = wrapper_->getClass()->getMethod<void(jint, ReadableNativeArray::javaobject)>("invoke");
然后我们去寻找JavaNativeModule类在java层对应的什么类。回到前面跟踪的路线，JsToNativeBridge的实例来自于NativeToJsBridge类的构造函数，而NativeToJsBridge的实例来自于Instance.cpp的initializeBridge方法，然后跟踪到CatalystInstanceImpl.cpp里的initializeBridge方法，这是个JNI方法，java层传过来的javaModules就是在这个函数里，被封装成了JavaNativeModule类。我们找到ReactAndroid/src/main/java/com/facebook/react/bridge/CatalystInstanceImpl.java里的initializeBridge方法，就知道C++中的JavaNativeModule对应了java中的JavaModuleWrapper类，这样最终我们就调用了JavaModuleWrapper类里的invoke方法。

### java调用js
源代码中有一个很好的从java调用js的例子，就是ReactRootView里的代码

    String jsAppModuleName = getJSModuleName();
    catalystInstance.getJSModule(AppRegistry.class).runApplication(jsAppModuleName, appParams);
从CatalystInstanceImpl.java的getJSModule方法里我们能看出，所有java能调用的js接口，都是继承自JavaScriptModule类，我们可以在项目中搜一下，就能默认有哪些类可以调用了，例如我们最常用的DeviceEventManagerModule。在JavaScriptModuleRegistry类中通过动态代理创建JavaScriptModule，这块我不太了解，所以只能跳过去了。实际我们调用的是JavaScriptModuleInvocationHandler类的invoke方法，它调用了CatalystInstanceImpl.java内的callFunction方法。然后通过PendingJSCall类的call方法，调用了

    catalystInstance.jniCallJSFunction(mModule, mMethod, arguments);
这是一个JNI方法，于是进入到了ReactAndroid/src/main/jni/react/jni/CatalystInstanceImpl.cpp内，然后来到ReactCommon/cxxreact/Instance.cpp的callJSFunction方法，然后是NativeToJsBridge的callFunction方法，再来到JSCExecutor的callFunction方法，在这里找到MessageQueue.js里的callFunctionReturnFlushedQueue方法调用。看messageQueue.js的__callFunction方法里，实现是

    const moduleMethods = this.getCallableModule(module);
哪些模块能够被调用，来自于MessageQueue类的registerLazyCallableModule，在Libraries文件夹内搜一下，就能找到Libraries/Core/InitializeCore.js。到这里就顿时清楚了，这些类在Java层中以继承自JavaScriptModule的interface形式记录下来，在js层中具体实现，然后按照上述流程最终执行js代码。