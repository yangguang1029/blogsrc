---
title: ReactNative之原生模块重名的问题
date: 2018-09-06 21:18:36
tags: ReactNative
---
在ReactNative开发中，封装原生模块几乎是必定要做的事情。原生模块分为两种：NativeModule和NativeComponent。对应的实现是

- iOS端NativeModule为实现RCTBridgeModule接口，NativeComponent为继承RCTViewManager类
- Android端NativeModule为继承ReactContextBaseJavaModule类，NativeComponent为继承SimpleViewManager或者ViewGroupManager类。

iOS端使用RCT_EXPORT_MODULE宏来指定模块名，这个名字是禁止重复的，如果重复在运行时会红屏报错。报错信息为

> Attempted to register RCTBridgeModule class XXX for the name "xxx", but name was already resgitered by class XXX

这段错误提示位于RCTCxxBridge.mm的registerModulesForClasses方法内。所以iOS端就不用担心什么了，一旦有模块名重复，运行会直接报错。

Android端通过重写getName方法来指定模块或者组件名，NativeModule是允许重名的，在BaseJavaModule类中有一个接口

    @Override
    public boolean canOverrideExistingModule() {
      // TODO(t11394819): Make this final and use annotation
      return false;
    }
如果后注册的重名模块重写了这个接口返回true，那么模块名允许重复，后添加的模块会覆盖掉先添加的模块。如果不重写或者这个接口返回false，则不允许重名，一旦重名会报错，报错信息位于NativeModuleRegistryBuilder.java内，在这里做了检测。

对于NativeComponent，虽然ViewManager也是继承自BaseJavaModule，但是它因为不走NativeModuleRegistryBuilder的流程，所以不会检测。不论是否重写canOverrideExistingModule接口，都允许重名，后添加的NativeComponent覆盖掉先添加的，这就是需要小心的地方，如果无意中写了两个重名的NativeComponent，先添加的就会被悄悄的覆盖了。