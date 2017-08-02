---
title: ReactNative之ref赋值应使用成员函数
date: 2017-08-02 20:18:36
tags: ReactNative
---

在线上项目收集的js error里，发现有一个问题，有的ref成员变量可能变为null,然后就出了问题。先看下面的代码。

	class Test extends Component{
		constructor(props) {
			super(props);
			this._ref = null;
		}

		render(){
			return (<View>
			<MyComponent ref={component=>this._ref=component}/>
			<Button onPress={this._onPress.bind(this)}/>
			</View>	
			)
		}

		_onPress(){
			this.setState({});
			this._ref.test();
		}
	}
当\_onPress被调用时，this._ref就可能变为null。

在facebook的[官方文档](https://facebook.github.io/react/docs/refs-and-the-dom.html)里，最后一段是一个警告信息
> If the ref callback is defined as an inline function, it will get called twice during updates, first with null and then again with the DOM element. This is because a new instance of the function is created with each render, so React needs to clear the old ref and set up the new one. You can avoid this by defining the ref callback as a bound method on the class, but note that it shouldn't matter in most cases.

可以很清楚的看到，如果ref函数每次都是一个新函数，就可能导致当render函数被执行时，ref被赋值两次，第一次被赋值为null，第二次才被赋值为需要指定的component。上面例子里我们在\_onPress函数里调用setState导致页面被重新渲染，然后\_ref被重新赋值，有比较小的几率\_ref会变为null，如果此时我们使用了_ref变量，就出现问题了。

解决的办法很简单，我们不应该让ref赋值函数每次都是新的函数，而不管是箭头函数，还是bind方法，每次都是生成一个新函数。所以我们在constructor函数里先绑定好一个成员函数来，然后使用它就可以了。这里就不写代码了，相信对js熟练的同学肯定很快就能写出来。