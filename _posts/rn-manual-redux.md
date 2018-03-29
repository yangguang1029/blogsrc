---
title: ReactNative之手动实现一个Redux
date: 2018-02-27 19:15:36
tags: ReactNative
---
最近我一直在考虑是否要移除项目中的redux使用，要做这个决定，首先是要搞明白redux的目的是什么，然后看看使用redux有哪些利弊。网上最适合了解redux的是[redux中文文档](http://www.redux.org.cn/)。

假设我们只有一个界面，那肯定不需要redux了，直接对this.state操作就行了，但如果有两个界面A和B，在A界面的操作需要改变B界面，在B界面的操作需要改变A界面，那么要么它们互相暴露接口，要么让它们把state放到共同的父组件里然后通过props传递下去，这样已经很复杂了，一旦有更多页面，它们之间互相影响，那就是一场噩梦了。要解决这个问题，就需要把数据和UI分离，所有界面渲染所需要的state，都存在一个大仓库里，这就是redux里的store。每个界面从仓库里取自己需要的state来进行渲染，当A界面的操作需要修改B界面时，它直接去修改仓库里B界面需要的数据，然后通知一下B界面刷新。在redux里是通过dispatch一个action来通知store修改数据的，如何修改则在reducer里实现，当reducer修改好数据后，会通知绑定了相关数据的界面执行setState进行界面刷新，这是通过react-redux提供的connect函数实现的。这就是redux做的所有事情，就仅此而已，我们可以很容易的自己实现，只需要实现一个数据中心，提供修改数据的接口，然后给页面提供监听即可。

为了避免描述不够清晰，以一个实际场景为例的话，我们有一些好友列表数据，那么我们实现一个FriendManager类，这个FriendManager做成全局单例对象，每个页面都可以调用它的接口。现在我们有个好友列表界面A，进入这个界面时还没有数据，我们需要显示loading界面，很简单，A界面直接来一个

    this.state = {isLoading:true, friends:[]}
就行了，不用像使用redux时考虑哪些state放到store里管理，哪些自己管理。

然后调用接口去像服务器请求数据，例如

    FriendManager.requestData();

为了收到数据后能够刷新界面，我们需要注册监听事件，例如

    NotificationCenter.addListener(UPDATE_FRIEND, this._updateFriend);

数据回来了，存储在FriendManager内，然后触发监听通知A界面

    NotificationCenter.trigger(UPDATE_FRIEND, data);

在A界面的回调函数里

    _updateFriend(data){
        this.setState({isLoading:false, friends:data})
    }
搞定，页面刷新了。现在我们有个好友详情界面B，在这个界面删除好友，这需要改变界面A，很简单，FriendManager提供一个接口

    FriendManager.removeFriend=function(friendID){
        this._friends.splice(...);
        NotificationCenter.trigger(UPDATE_FRIEND, this._friends);
    }
B界面调用这个接口，A界面就收到通知进行刷新了，不管AB界面隔得多遥远，也不管有多少个界面会互相影响，他们没有任何耦合。

redux基于这个核心目的做了一些优化，例如使用action来代替直接调用FriendManager内的方法，这样可以更加清晰明了，开发者很明确要做一件什么事情。但抽象成action是有代价的，开发者需要理解action的概念，然后需要实现很多生成action的方法。像redux三大原则（单一数据源，state只读，reducer为纯函数），再加上middleware, sagas，immutable.js等等，很多人就晕头转向了，这就是我认为的使用redux的弊端吧，我们的项目一开始就引入了redux，但搭了个框架后，大家都不用，又要写action，又要写reducer，还要去connect，就算写了，也不考虑immutable原则。所以还是看项目的实际情况吧，如果确实不是很复杂的场景，例如上面举的好友列表数据管理方案，其实自己实现倒更直观。