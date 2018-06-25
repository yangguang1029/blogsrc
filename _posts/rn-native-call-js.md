---
title: ReactNative之快速实现native调用js
date: 2018-05-23 20:18:36
tags: ReactNative
---
在官方文档里推荐的原生调用js的方法是通过发送事件，也就是通过DeviceEventEmitter来发送事件，然后在js层监听。这样虽然可以实现，但毕竟感觉有点绕弯，实际上观察一下源代码就会发现原生层有直接调用js的接口。它们分别是：

iOS端位于RCTBridge中

    - (void)enqueueJSCall:(NSString *)module method:(NSString *)method args:(NSArray *)args completion:(dispatch_block_t)completion;
Android端位于CatalystInstance中

    void callFunction(String module, String method, NativeArray arguments);
可以看到要调用js代码，都需要一个模块名和方法名，然后是传入的参数。被原生调用的接口，需要在js代码中进行注册，注册的代码例如：

    const BatchedBridge = require('BatchedBridge');
    BatchedBridge.registerCallableModule('hello', {
        world:function(){
            console.log("hello world");
        }
    });
这样在调用时，module就是"hello"，而method就是"world"了，当然调用前要先想办法获取到RCTBridge和CatalystInstance实例，这个对于RN有一定了解程度的同学来说肯定不是什么难事了，RCTBridge可以在初始化时存起来，CatalystInstance在初始化时通过ReactInstanceManager可以获取到。试试看吧，是不是感觉比发送事件监听事件要方便很多呢，不用再想着应该什么时候注册监听，什么时候取消监听了。


