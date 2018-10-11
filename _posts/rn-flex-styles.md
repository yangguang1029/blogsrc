---
title: ReactNative之flex属性值
date: 2018-10-10 21:18:36
tags: ReactNative
---
之前就看过一个例子，是下面的这种情况

```
<View style={{width:200,height:200}}>
  <View style={{flex:1, height:150, backgroundColor:'red'}}/>
  <View style={{flex:1, height:150, backgroundColor:'blue'}}/>
</View>
```
大家可以自己跑一下，就会发现这两个子组件最后各自高度是100。但如果把两个flex:1改成flexGrow:1，就会发现它们高度变成了150。读完以下的内容，就能知道是什么原因了。

在RN开发中，我们可以设置flex为一个数值x，它实际上是一个简写，相当于flexGrow:x flexShrink:1 flexBasis:0。下面介绍一下这三个值，我们默认父容器的flexDirection为column，这样子元素是纵向排列，动态变化的就是高度height。

**flexBasis**
它用于设置当前元素的尺寸，作用和height或者width一样，但优先级更高。flexBasis可以设置为数字，或者百分比字符串，也可以是auto。默认值为auto。当flexBasis和height之一为auto时，则另一个非auto值优先级更高。

**flexGrow**
它用于当元素尺寸之和小于父容器尺寸时，动态分配父容器剩余空间，默认值为0。例如父容器高度200，两个子组件高度各为50，此时剩余空间为100，此时第一个组件设置flexGrow为1，则它会独占所有的剩余空间，高度为150。如果再将第二个组件设置flexGrow为3，那么剩余空间按1:3分配，两个组件高度为75和125。

**flexShrink**
它和flexGrow相反，用于当元素尺寸之和大于父容器尺寸时，动态压缩自身大小，默认值为0。例如父容器高度为200，两个子组件高度各为150，此时需要压缩空间为100，如果第一个组件设置flexShrink为1，那么压缩空间都由它负责，高度变成了50，如果再将第二个组件设置flexShrink为1，那么压缩空间各负责一半，两个组件高度都为100。

回到一开头的问题，就很清楚了，之所以设置flex为1时会两个子组件高度为100，是因为flex:1等于flexGrow:1,flexShrink:1,flexBasis:0，前面说过flexBasis优先级高于height，所以两个子组件设定的高度为0，那么就有200的剩余空间用于分配，因为flexGrow都为1，则各占一半。而将flex:1改为flexGrow:1，因为没有设置flexBasis，所以height:150将生效，又没有设置flexShrink，所以不会进行压缩，所以各自高度为150。

另外需要注意一种特殊情况，就是flex设为0，它意味着组件inflexible，不再动态调节，而是按照width或height来显示。可以试着把上面的例子改成第一个组件flex:0，第二个组件flex:1，会发现第一个组件先占了150高度，然后第二个组件因为flexBasis为0，flexGrow为1，所以他会占掉全部剩余的50高度。

还有就是flex为负数的情况，当flex设为负数时，会按照设定的width或者height来显示，如果父组件空间不够，则会压缩到minWidth或者minHeight尺寸。对此我们可以做一下实验，将第一个组件flex设为-10，height设为50，第二个组件flex设成1，height设为50，此时第一个组件按照50高度显示，而第二个组件因为flexGrow:1占用了所有的剩余空间，所以高度为150

最后是列举一些测试用的例子，并分析原因

```
<View style={{width:200,height:200}}>
  <View style={{flex:-1, height:250, backgroundColor:'green'}}/>
  <View style={{flex:1, height:50,  backgroundColor:'black'}}/>
```
第一个组件占用200高度，第二个组件看不见。因为第一个组件需要按照250高度显示，但被压缩到了minHeight:200，第二个组件flexBasis为0，flexGrow为1，因为没有了剩余空间，所以不显示。如果第一个组件添加minHeight:250，那么就不会被压缩，显示为250高度。（如果minHeight设为300，则占满了屏幕高度，显然是不正常的，但不做深究，毕竟设置minHeight>height是不合理的）

```
<View style={{width:200,height:200}}>
  <View style={{flex:-1, height:250, backgroundColor:'green'}}/>
  <View style={{flex:0, height:50,  backgroundColor:'black'}}/>
```
两个组件都需要按照实际高度显示，但第二个组件flex为0优先级更高，它先占用了50的高度，然后第一个组件被压缩到了150的高度。如果给他设置minHeight，则会按照minHeight高度显示
