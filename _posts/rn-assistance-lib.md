---
title: ReactNative之辅助库选择
date: 2018-08-29 21:18:36
tags: ReactNative
---
很多刚入门RN开发的同学面对着老鸟侃侃而谈什么redux,immutable,saga这些库是一脸懵逼的状态，拿不准自己开发的时候是否该用，这里我列举一下我自己的意见。为了篇幅和容易理解，不会说的太详细和深入，像服务器渲染这种就不提了（其实是因为我也不是很懂……）

### Redux
**收益**
1. 单向数据流的方式有利于管理，不用到处传递prop了
2. 有利于解耦，使用redux的话天然就将model从view中解耦了出来
3. 有利于state跟踪和现场还原

**代价**
1. 学习成本。action,reducer,store,middleware等概念，dispatch, connect等API接口
2. 增加代码量和操作复杂度，一个state要伴随着actionType, createAction, reducer, connect等等，涉及到至少三四个文件

**是否会影响性能**

有人担心使用redux会影响性能，不可否认，增加了这么多概念和接口，使用不当肯定会造成性能影响。但关键就是看你怎么用。有一篇文章[redux-ruins-you-react-app-performance-you-are-doing-something-wrong](https://itnext.io/redux-ruins-you-react-app-performance-you-are-doing-something-wrong-82e28ec96cf5)可以仔细看一下，举个例子，使用react-redux可以给组件绑定特定的一些state，只有这些state发生了变化才会re-render，相比使用传递prop的方案是有利于性能提高的，因为prop传递经过的中间组件可能产生了不必要的re-render，但如果mapStateToProp写的不好，里面有大量复杂的计算，就会导致性能产生问题，因为每个mapStateToProp函数在state发生了变化都会被调用，这时就需要使用reselect库来进行优化，或者在connect时使用areStatesEqual选项。总的来说，redux作为一个使用如此广泛的库，只要正确使用，肯定不用担心会影响性能。

**state如何管理**

网上有过一些争论，是否应该把所有的state都集中到store中管理。[官方文档](https://redux.js.org/faq/organizingstate)的说法是：没有对错，你自己看着办。把所有的state都集中到store中管理，这其实是一种比较理想的状态，所有的组件都是无状态组件，但这也导致state的规模变得臃肿和难维护。在实际开发中也没必要追求达到这种境界，一个state是否放到store里去，根据一些原则判断即可：
1. 是否需要持久存储
2. 是否需要公共使用
3. 是否需要场景还原

**是否使用**

redux的[官方文档](https://cn.redux.js.org/)推荐一篇文章[you-might-not-need-redux](https://medium.com/@dan_abramov/you-might-not-need-redux-be46360cf367)，大概就是说redux本身只是一个辅助工具，用或者不用取决于你自己衡量得失，最重要的是理解它的思想。例如对于简单一些的项目，不使用redux也可以自己按照其思路写出redux风格的代码，我曾经就有过这样的想法：[ReactNative之手动实现一个Redux](http://yangguang1029.github.io/2018/02/27/rn-manual-redux/)

### Immutable
redux的三原则之一就是state不可变原则，使用immutable就是借助工具来保障，如果不使用，则需要靠开发人员自己保证，比如使用Object.assign

**收益**
1. 不可变保障：其对外提供的API可以保证必然是生成新对象
2. 效率更高：对于深层次的局部更新，immutable库的内部实现效率更高

**代价**
1. 新的API的学习和使用成本。如果不使用，直接操作的是js的原生API，使用immutable，只能使用库提供的API来操作array, object等
2. immutable代码会扩散到整个项目。从state获取到的数据是immutable对象，所以immutable的API会扩散在整个项目中

**是否使用**

如果state结构比较扁平，那可以人为保障不可变性。如果state纵深结构比较复杂而且reducer拆分不够细，那最好还是使用，否则的话各种该刷新却不刷新，不该刷新却刷新的小问题就层出不穷了。如果使用的话一般会选择[seamless-immutable](https://github.com/rtfeldman/seamless-immutable)

### Redux-saga
异步action的处理，有redux-thunk和redux-saga，redux-promise，redux-observable等多种方案，因为熟悉程度，所以本文只比较前两者。

**收益**
1. 相比redux-thunk来说，saga使用的async,await语法可以让异步操作代码流畅易懂，避免promise地狱
2. 使用saga方便做单元测试
3. redux提供throttle, 取消任务，监听未来action等多种高级功能，适合复杂场景

**代价**
1. 学习成本。async和await本身就没那么普及，还多出来各种effect。
2. redux-saga库压缩前59k，压缩后24k。要么通过拆分bundle方案放到基础bundle中，否则每个业务bundle中都有一份显然增加bundle体积。

**是否使用**

取决于异步操作流程的复杂度，例如一个向服务器获取数据的异步操作，需要先向原生层获取若干个数据，然后向服务器获取配置信息，然后才去请求数据，之后还要通过原生层做本地存储等等，一个流程有一系列的异步操作，那么使用saga绝对是值得的，代码看起来神清气爽。如果异步操作不多而且流程不是很复杂，一两个promise就结束了，那就别多费事了，毕竟码农主业是搬砖，不是炫技。