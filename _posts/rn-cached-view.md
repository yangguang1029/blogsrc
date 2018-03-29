---
title: ReactNative之一个组件缓存的方案
date: 2018-03-12 20:18:36
tags: ReactNative
---
在实际开发中，我们经常会有这样的场景，一个组件需要根据条件来决定显示还是隐藏，我们一般都不假思索就可以写出这种方案

    this.state.isVisible ? <MyComponent /> : null
一般来说这样做都没什么问题，但假如这个MyComponent非常庞大，而显示隐藏又很频繁，这样做性能就很低，根据前面的一篇博文[《ReactNative之VirtualDomTree的diff原理》](http://guangy.coding.me/2018/02/25/rn-reconciliation/)，实际上我们把一个组件在不同的类型MyComponent和null之间切换，是一定会导致MyComponent每次都被重建和销毁的。

那我们就想办法实现一下缓存，根据实际测试，发现有一个比较简单的方案，当我们希望隐藏时，把MyComponent的尺寸设为0即可，例如组件是沿竖轴排列，只要调节MyComponent的高度即可，所以这个方案只适用于能确定尺寸的情况。

使用这个方案，MyComponent在显示和隐藏之间切换时，组件本身不会被销毁，我们接下来就是尽量减少re-render的触发，以提高性能。当尺寸变化时，MyComponent无疑必须触发re-render，如果它的所有子组件都是普通Component的话，那么也会相应触发re-render。所以最简单的方案，我们把它的子组件改成PureComponent，这样只要MyComponent的尺寸没有通过props传递下去，子组件就不会re-render。如果要更加灵活的话，我们就实现子组件的shouldComponentUpdate即可。

我们实际项目中有一个选择表情的组件，它包含了100多个小表情，当这个组件显示和隐藏时，原来都有一定延迟，通过使用这个优化方案，性能得到了很大提高。[如果不是很明白，可以参考一下我写的demo](https://github.com/yangguang1029/MyReactNative/blob/master/testCacheView.js)