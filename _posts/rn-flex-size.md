---
title: ReactNative之组件自适应尺寸
date: 2018-08-23 19:15:36
tags: ReactNative
---
组件如果不设定尺寸的话，会按照一定的规则，随着父组件和子组件的尺寸自适应。首先我们确定一个前提，父组件和子组件都是有尺寸的。除非明确设定尺寸为0，否则一个组件肯定是有尺寸的，对于根组件，它的父组件实际上是整个屏幕大小flexDirection为column的一个组件。

首先是适应父组件的规则，当一个组件不设置尺寸且没有子组件，它的尺寸取决于父组件的尺寸和flexDirection。如果flexDirection为row，那么它的宽度为0，高度为父组件的高度。如果flexDirection为column，那么高度为0，宽度为父组件的宽度。因为宽或者高为0，所以不会显示。

然后是适应子组件的规则，当一个组件不设置尺寸且有子组件，那么它会适应子组件的宽高。例如父组件flexDirection为row，那么它的宽度为子组件的宽度，高度为父组件的高度。如果flexDirection为column，那么高度为子组件的高度，宽度为父组件的宽度。

当给组件设置了尺寸，但只有宽或者高，那么缺少的那个会按照上面的规则来自适应，例如父组件flexDirection为row，那么给它设置高度，就会按此高度显示，否则就按父组件高度显示，如果设置宽度，则按此宽度显示，否则由子组件宽度决定。

以上三条规则，可以自己写个简单demo验证测试。熟悉了这些规则，在实际开发中，对于尺寸不固定的组件，布局起来就不容易出问题了。

顺便提一下，原生组件在原生层设置尺寸是不会生效的，组件大小完全取决于js层设置style。在iOS平台，RN给UIView加了一个category  UIView (React)，里面有一个reactSetFrame方法，我们可以给原生组件view实现这个方法来监听它的尺寸，验证上面的规则。
