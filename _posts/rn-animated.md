---
title: ReactNative之Animated使用
date: 2018-09-12 21:18:36
tags: ReactNative
---

需要注意的是：
1. 赋值必须使用new Animated.Value
2. 需要显示动画的组件加上Animated前缀，例如Animated.View, Animated.Text, Animated.Image, Animated.ScrollView
3. reset时不时使用setState来重新赋值，而是使用this.state.xxx.setValue
4. 可以操作的属性包括style上的opacity,width,height,left,top,right,bottom