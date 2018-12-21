---
title: ReactNative之mapStateToProps
date: 2018-12-18 21:15:36
tags: ReactNative
---
connect是react-redux库提供的一个辅助函数，它的第一个参数是mapStateToProps，官方文档对这个函数的介绍很清晰：

> 如果定义该参数，组件将会监听 Redux store 的变化。任何时候，只要 Redux store 发生改变，mapStateToProps 函数就会被调用。该回调函数必须返回一个纯对象，这个对象会与组件的 props 合并。如果你省略了这个参数，你的组件将不会监听 Redux store。如果指定了该回调函数中的第二个参数 ownProps，则该参数的值为传递到组件的 props，而且只要组件接收到新的 props，mapStateToProps 也会被调用（例如，当 props 接收到来自父组件一个小小的改动，那么你所使用的 ownProps 参数，mapStateToProps 都会被重新计算）。

首先有一个问题，这个函数只要state发生变化就会被调用，然后又返回了一个纯对象，会让人担心是否组件不关心的state部分变化了，也会导致自己刷新呢？答案显然是否定的，mapStateToProps返回的这个对象是拿去做了浅比较。如果浅比较发生不相等，就会导致组件刷新，否则不会（当然我们暂时忽略自定义了shouldComponentUpdate的情况）。我们说的浅比较，就是RN源代码里的shallowEqual,它的实现是浅比较两个对象的所有值。

对下面这个简单的例子而言

    const mapStateToProps = (state, ownProps) => {
      return {
        world: state.world[0]
      }
    }
因为我们在这个函数里只关注了state.world，所以state的其它属性变化虽然也会导致这个函数被调用并返回了一个新对象，但因为返回的新对象浅比较相等，所以不会刷新组件。对于state.world来说，我们这里关注的是state.world[0]，而不是state.world本身，所以如果state.world本身发生了变化但是state.world[0]没变，那也不会刷新，如果state.world本身没变，但是state.world[0]通过发生了变化，那也会刷新组件。虽然说的绕口但只要记住它的原理就行，我们是拿这个函数里返回的这个纯对象去执行shallowEqual的。

因为只要state发生了变化这个函数就一定会被调用，所以如果这个函数里有复杂的计算，就需要考虑memoization。实现的方式一个是通过[reselect库](https://cn.redux.js.org/docs/recipes/ComputingDerivedData.html)，另一个是在connect时，设置它的第四个参数options，这个参数的areStatesEqual属性是一个函数，返回true或者false来决定state是否发生了变化，从而决定mapStateToProps是否会被调用，而我们上面提到的mapStateToProps返回的纯对象是进行了浅比较，也是这里areStatePropsEqual属性决定的，它是一个函数，默认值是shallowEqual。了解options参数更多可以参见[这篇博客](https://medium.com/@ryansperzel/reduxs-connect-function-and-arestatesequal-option-adc97e00ee0)