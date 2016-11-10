---
title: 重用ccnode需要注意的触摸事件处理
date: 2016-08-15 20:39:37
tags: cocos
---
在使用cocos开发过程中，对node的重用非常常见，例如TableViewCell就是重用的，这些被重用的node会频繁的被添加到父节点以及从父节点中移除，当被移除时会调用

```
removeFromParent(cleanup)
```

这个cleanup参数很关键，如果为true，会导致其cleanup方法被调用。如果不带此参数，则默认为true。

```
cleanup: function () {
    this.stopAllActions();
    this.unscheduleAllCallbacks();
    cc.eventManager.removeListeners(this);
    this._arrayMakeObjectsPerformSelector(this._children, cc.Node._stateCallbackType.cleanup);
    }
```

可以看到，所有被加到此节点上的eventListener都被清除掉了，同时还递归调用了所有子节点的cleanup方法，也就意味着**一个node执行了cleanup的话，其自身以及所有子孙结点注册的eventListener都会被移除**。在重用这个node时，很可能就会发现给它添加的eventListener不生效了。

但cocos对一些node做了相应的功能完善，专门针对的是触摸事件。在其添加触摸事件时，用成员变量_touchListener保存起来，在onEnter时重新添加。这也是我们在碰到此类问题时的解决方案。cocos只对三个类做了这种实现，他们是cc.Control, cc.Menu, ccui.widget。理所当然的，继承自这三个类的也都有此功能，例如cc.ControlButton被重用时，它的触摸事件不会消失。

有人会说，tableViewCell一直在被重用，也不继承自上面三个类，为什么对它的触摸回调tableCellTouched一直能生效呢？这是因为tableCellTouched并不是在tableViewCell上添加的触摸事件，而是在tableView上添加的，如果你尝试重用tableView或者其父容器，就会发现触摸失效了，我的解决方案是重用时调用一次tableview的setTouchEnable接口。

总之在实现重用node时，要注意添加给它和它的子孙节点的事件，需要在onEnter时重新添加，例如某个节点的一个子孙节点是一个cc.TableView，那么在重用这个节点时，这个tableview的触摸肯定失效了，解决办法要么修改源代码在tableView的onEnter方法里重新添加，或者在重用时手动调用tableview的setTouchEnabled方法（这个方法继承自scrollview）