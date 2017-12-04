---
title: ReactNative之重叠区域触摸处理
date: 2017-11-15 19:18:36
tags: ReactNative
---
在做界面时，写了一个弹窗界面，它有个全屏的半透明背景，只是一个普通的View，当弹窗弹出时，发现原来界面的所有触摸都失效了，就像这个半透明背景把触摸都吃掉了一样，按照原来用cocos的习惯，一个普通的View如果不去指定接受触摸，应该不会处理触摸，而是将触摸传递给下一层界面才对。

为了确定RN的触摸传递机制，写了个demo试验了一下。就不贴代码了，很简单，界面上写两个View分别是A和B，他们区域重叠且A被B覆盖，给他们都设定onStartShouldSetResponder接口，只有这个接口返回true，才会感受到触摸。可以观察到，无论B的onStartShouldSetResponder返回true还是false,当触摸发生在重叠区域时，A的onStartShouldSetResponder都不会被回调。这样结论就很明显了，**同级组件如果有重叠区域，则重叠区域内触摸事件完全由后渲染组件接受，先渲染组件连是否接受触摸的回调都不会被调用，不可能有机会处理触摸**

然后是父子节点，触摸父子节点的重叠区域，子节点的onStartShouldSetResponder会先被调用，如果子节点的onStartShouldSetResponder返回了true，那么父节点的onStartShouldSetResponder将不再被调用，也就是父节点没有机会响应触摸，如果子节点的onStartShouldSetResponder返回了false，那么父节点的onStartShouldSetResponder会被调用，此时子节点忽略触摸，交由父节点处理。

如果区域不重叠，那显然各干各的，如果重叠，则是遵循上面的原则。所以再看最开始那个例子，这个弹窗有个全屏背景，即使只是一个普通View，没有写任何触摸相关的代码，他也会把同级节点的触摸事件全部屏蔽了。如果一定要让触摸传递下去，可能只能想办法hack了，比如修改层级关系。