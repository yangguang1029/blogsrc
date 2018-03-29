---
title: ReactNative之MessageQueue
date: 2018-02-09 20:18:36
tags: ReactNative
---
MessageQueue的代码位于react-native/Libraries/BatchedBridge/MessageQueue.js中。在ReactNative中，MessageQueue的作用是负责js和native端通信的连接桥梁，也是唯一的桥梁，所有的js端和native端交互，都经过了MessageQueue，例如点击一个按钮，感受触摸是在native端，回调函数执行在js端，这是一次native到js端的通信，如果在回调函数中移动一个component的位置，因为渲染在native端，所以需要一次js到native的通信。确保MessageQueue运行通畅，可以避免应用出现性能问题。

MessageQueue有个接口，允许我们在log里查看通信记录，开启方式为

    import MessageQueue from 'react-native/Libraries/BatchedBridge/MessageQueue'
    MessageQueue.spy(true);

在控制台看到的输出日志例如：

    JS->N : UIManager.createView([10,"RCTView",41,{"flex":1,"pointerEvents":"box-none"}])
    JS->N : UIManager.setChildren([10,[9]])
    JS->N : UIManager.setChildren([41,[10]])
    N->JS : RCTDeviceEventEmitter.emit(["appStateDidChange",{"app_state":"active"}])
    N->JS : <callback for AppState.getCurrentAppState>([{"app_state":"active"}])
    N->JS : RCTDeviceEventEmitter.emit(["websocketFailed",{"message":"Failed to connect to localhost/127.0.0.1:8097","id":0}])
    JS->N : Timing.createTimer([1,2000,1518145067893,false])
    N->JS : JSTimers.callTimers([[1]])
    JS->N : WebSocketModule.connect(["ws://localhost:8097",null,{"headers":{}},1])
    N->JS : RCTDeviceEventEmitter.emit(["websocketFailed",{"message":"Failed to connect to localhost/127.0.0.1:8097","id":1}])
    JS->N : Timing.createTimer([2,2000,1518145069380,false])
    N->JS : RCTEventEmitter.receiveTouches(["topTouchStart",[{"identifier":0,"locationY":6.25,"locationX":223.2421875,"pageY":6.25,"timestamp":18767831,"target":3,"pageX":223.2421875}],[0]])
    JS->N : Timing.createTimer([3,130,1518145070239,false])
    JS->N : Timing.createTimer([4,500,1518145070240,false])
    JS->N : UIManager.setJSResponder([4,false])

JS线程和UI线程是不同的线程，所以这种通信都是异步的。因为RN的内部优化，UI线程很少出现卡死，我们在实际开发中容易碰到的问题是MessageQueue通信不顺畅，表现就是UI响应迟钝。有可能我们在js中写了个死循环，这导致MessageQueue彻底瘫痪，或者我们通过MessageQueue执行了太多交互，或者交互时传递大量数据，造成MessageQueue堵塞。我们通过一个例子来观察这种情况下的表现

    _delay(seconds) {
        let now = new Date().getTime();
        while(true) {
            if(new Date().getTime() - now >= seconds * 1000){
                break;
            }
        }
    }
    render(){
        return <View>
            <Button title="A" onPress={()=>{
                console.log("guangy press........1")
                this._delay(8);
            }}/>
            <Button style={{marginTop:20}} title="B" onPress={()=>{
                console.log("guangy press........2")
            }}/>
        </View>
    }
当点击按钮B时，可以正常的点击响应，但如果点击A按钮后再点击B，就会发现没有任何反应，直到8秒后，B按钮才透明度变化并输出log，这是因为_delay函数里的无限循环把js线程卡死住，native层感受到了触摸，然后把事件发送到js层，但因为js层没有机会处理它，而Button的透明度变化是在js代码里改变的，所以现象就是按钮没有任何反应，当8秒后无限循环结束，事件才被处理，于是按钮点击效果出现，如果在点击按钮A后多次点击按钮B，这些事件会被堆积下来，然后响应多次。

然后可以试验一下把MessageQueue堵塞的情况，例如

    _busy(){
        for(let i = 0; i < 10000; i++) {
            setTimeout(()=>{}, 10)
        }
    }
点击按钮A后调用_busy函数，它连续创建10000个setTimeout，setTimeout的实现是通过MessageQueue从js端往native发送信息，最终调用Timing类的createTimer方法。这样短时间内
