---
title: ReactNative之PureComponent
date: 2017-12-21 18:18:36
tags: ReactNative
---

首先把官方文档对于PureComponent的介绍搬过来，如果看明白了，就可以直接结束本文了：）

> React.PureComponent is similar to React.Component. The difference between them is that React.Component doesn’t implement shouldComponentUpdate(), but React.PureComponent implements it with a shallow prop and state comparison.
> 
> If your React component’s render() function renders the same result given the same props and state, you can use React.PureComponent for a performance boost in some cases.
> 
> 
> React.PureComponent’s shouldComponentUpdate() only shallowly compares the objects. If these contain complex data structures, it may produce false-negatives for deeper differences. Only extend PureComponent when you expect to have simple props and state, or use forceUpdate() when you know deep data structures have changed. Or, consider using immutable objects to facilitate fast comparisons of nested data.
> 
> Furthermore, React.PureComponent’s shouldComponentUpdate() skips prop updates for the whole component subtree. Make sure all the children components are also “pure”.

PureComponent和Component的唯一区别就是shouldComponentUpdate方法

	//Component
	shouldComponentUpdate(nextProps, nextState){
		return true;
	}
	//PureComponent
	shouldComponentUpdate(nextProps, nextState){
		return this.props !== nextProps || this.state !== nextState;
	}
当props或者state发生了变化时shouldComponentUpdate会被调用，如果返回true则触发re-render，否则不会。 这里说的发生了变化，不一定是指内容或者引用发生了改变，只要调用了this.setState就认为是发生了变化，而只要父组件触发了re-render，就认为props发生了变化。

Component采用的默认实现是直接返回true，意味着只要props或者state发生了变化就会re-render。
PureComponent则是进行了一次浅比较(shallow comparison)，只有当props和state之一在引用上发生了变化，才会re-render。

PureComponent相比Component减少了re-render的可能性，所以一定程度上可以优化性能。一个很明显的例子就是在使用flatList的时候。假设flatList当前渲染了第0-200个单元行，滑动后需要渲染第0-201个单元行，这是通过flatList的setState来刷新的，因为父组件flatList触发了re-render，所有的子元素也就是单元行组件，都会触发shouldComponentUpdate。如果单元行组件继承自Component，那么第0-200个单元行都会触发re-render，总共201次render。但如果继承自PureComponent，那么只会触发第201个单元行的render，总共只有1次render。这可以通过写一个小demo进行验证。

PureComponent虽然可以减少re-render，但也有坑，那就是它在shouldComponentUpdate里进行的是浅比较，也就意味着如果props和state是一个复杂对象的引用，那么它的内容变了但是引用本身没变，此时可能需要触发re-render却没有触发。

PureComponent适合用于props和state比较简单的组件，否则的话应该使用Component并重写componentShouldUpdate方法，既能减少re-render，又能避免错过re-render。

