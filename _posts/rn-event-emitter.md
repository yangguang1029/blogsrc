---
title: ReactNative之EventEmitter
date: 2018-05-28 20:18:36
tags: ReactNative
---
官方文档推荐的原生往js层传递消息的方式，[iOS端](https://reactnative.cn/docs/0.51/native-modules-ios.html#%E7%BB%99javascript%E5%8F%91%E9%80%81%E4%BA%8B%E4%BB%B6)是继承RCTEventEmitter，然后调用sendEventWithName方法

    [self sendEventWithName:@"EventReminder" body:nil];

[Android端](https://reactnative.cn/docs/0.51/native-modules-android.html#%E5%8F%91%E9%80%81%E4%BA%8B%E4%BB%B6%E5%88%B0javascript)是

    getReactApplicationContext()
                .getJSModule(DeviceEventManagerModule.RCTDeviceEventEmitter.class)
                .emit("EventReminder", null);

Android端一眼就能看出来是通过RCTDeviceEventEmitter模块来交流的，所以在js层直接使用RCTDeviceEventEmitter来注册监听。例如

    var emitter = require("RCTDeviceEventEmitter")
    emitter.addListener("EventReminder",(e)=>{
      console.log("guangy get event in RCTDeviceEventEmitter")
    })
或者

    import {DeviceEventEmitter} from "react-native"
    DeviceEventEmitter.addListener("EventReminder",(e)=>{
      console.log("guangy get event in DeviceEventEmitter")
    })
但是在iOS端就会发现这两个回调都不管用了。实际上去RCTEventEmitter类里面看一下它的sendEventWithName方法，发送事件的代码是

    if (_listenerCount > 0) {
        [_bridge enqueueJSCall:@"RCTDeviceEventEmitter"
                    method:@"emit"
                      args:body ? @[eventName, body] : @[eventName]
                completion:NULL];
    }
其实也是通过RCTDeviceEventEmitter发送的消息。但这里有个if判断，_listenerCount的初始值为0，下个断点就很快发现，没有进到if里去。使用NativeEventEmitter来注册监听，就可以收到了

    const Test = NativeModules.TestNative;
    const testEmitter = new NativeEventEmitter(Test);
    const subscription = testEmitter.addListener('EventReminder',
        ()=>{
            console.log("guangy get event in NativeEventEmitter");
        }
    );
看一下NativeEventEmitter的代码很快就能找到原因，在它的addListener方法里，有

    if (this._nativeModule != null) {
      this._nativeModule.addListener(eventType);
    }
这是调了原生模块的addListener方法，在RCTEventEmitter类中它的实现就是让_listenerCount加1。所以在iOS端，因为原生代码中通过继承RCTEventEmitter类来发送消息，js层就必须使用NativeEventEmitter来注册监听，否则的话，原生层连消息都不会发出去。但是在Android端，因为底层实现就是直接给RCTDeviceEventEmitter发消息，不像iOS端有RCTEventEmitter类的那一套逻辑，所以三种注册监听的方式都一样，构造NativeEventEmitter实例时，也可以不传递NativeModule参数。

如果iOS的原生层不使用RCTEventEmitter，那么就和Android端一样可以直接使用RCTDeviceEventEmitter监听，例如

    [self.bridge.eventDispatcher sendDeviceEventWithName:@"EventReminder" body:nil];
但这个接口已经被废弃了，所以不建议使用。要么直接套用sendEventWithName的if里面的实现

    [self.bridge enqueueJSCall:@"RCTDeviceEventEmitter"
                  method:@"emit"
                    args:@[@"EventReminder"]
              completion:NULL];
这样也可以直接使用RCTDeviceEventEmitter来监听。

到这里结论就清楚了，**我们在js层应该使用NativeEventEmitter，这是双端统一的事件传递接口**。

我们再看一下NativeEventEmitter.js里的实现，它的构造函数里有一句

    super(RCTDeviceEventEmitter.sharedSubscriber);
这就很明显了，虽然我们在js层可以给每个模块都new一个NativeEventEmitter，但实际上它们都是交给了RCTDeviceEventEmitter来处理，这也跟原生代码中是通过调用RCTDeviceEventEmitter模块的emit来发送消息是一致的。js层所有的注册都在EventSubscriptionVendor.js中进行管理，实现也很简单，就是通过字典存储事件名和回调函数列表。

在js层还有一个类RCTNativeAppEventEmitter，不过已经被声明废弃了，所以忽略掉。

最后我稍微想了一下，如果不使用NativeEventEmitter的话，其实代码更简单，不用考虑remove取消监听，双端也是统一的。但为什么iOS平台废弃掉直接发送事件的接口，然后统一使用NativeEventEmitter呢？我能想到的优点就是原生层可以通过startObserving和stopObserving来监听某个事件的监听状况，然后虽然本质上事件仍然都是扔到了RCTDeviceEventEmitter来处理，但至少从代码上进行了隔离，将事件和模块绑定起来，避免了混杂。
