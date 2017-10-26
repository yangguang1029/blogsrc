---
title: ReactNative中的Component的生命周期
date: 2017-10-21 19:15:36
tags: ReactNative
---

本文介绍一下Component生命周期相关的一些函数，主要参考自[官方文档](https://reactjs.org/docs/react-component.html) 

### render
render函数是必须实现的，它用来渲染界面。一般会由this.props和this.state来控制如何显示。在这个函数里不能调用setState，否则会导致死循环，因为setState会导致render被调用。
render函数返回true,false,null,undefined都是合法的jsx语法，但它们都不会产生渲染。render函数应该避免太复杂耗时的操作。另外注意一下<Text></Text>组件里如果想显示bool值,null,undefined时也需要显示转换成字符串才行。

## mount

### constructor
构造函数是最早被调用的，构造函数的第一句应该是super(props)。 state的初始化应该放在构造函数里。当然还有声明类的成员变量。

### componentWillMount
当Component将要被加载时被调用，它在render之前被调用。在这个函数里执行setState的话，不会触发componentWillUpdate和render。因为render还没被调用，所以在这个函数里想通过ref获取子控件是不行的。componentWillMount为第一次render提供了准备数据的机会，我们可以放心的操作props和state。

componentWillMount也适合用来注册事件监听，假如有的事件在渲染时触发，那么在render前就注册显然更合适。

### componentDidMount
当component已经被加载后调用，它在render之后被调用。所以在这个函数里执行setState会触发componentWillUpdate和render。对于同级节点，先渲染的componentDidMount会先被调用，对于父子节点，子节点的componentDidMount会比父节点先调用。前面说到render不应该调用setState来触发re-render，而componentWillMount调用setState又不会触发re-render，显然componentDidMount则完全没问题了，比如我们有一个component的尺寸未知，取决于另一个component的已知尺寸，就可以在componentDidMount里获取数据，计算好后setState来重新render。

### constructor，componentWillMount和componentDidMount分别适合做什么事情
constructor显然适合做初始化，比如初始化state,成员变量，绑定成员函数等。而componentWillMount和componentDidMount的主要区别就是一个在render前，一个在render后。如果需要处理原始props和state，就应该放到componentWillMount中，比如使用props给state赋值，此外注册监听适合放在componentWillMount内。除此之外，大多数情况下的操作应该放到componentDidMount里，比如发起异步请求，开启计时器等等。

## update

### componentWillReceiveProps(nextProps)
当component的props被更新时被调用，但需要注意的是，update流程的所有回调触发的前提都是有update，也就是我们在父控件代码中改变子控件props但不触发update的话，这个回调也不会被调用的。例子很简单，比如

	render(){
		return (<View>
			<TestComponent num=this._num>
			<Button onPress={()=>{this._num=999}}>
		</View>)
	}
点击按钮改变了this.\_num，而this.\_num又作为TestComponent的props传递进去了，但因为并没有触发update，所以TestComponent的任何update回调都不会被触发。

另外需要注意，该回调被调用时，不一定props发生了变化，这里的没有发生变化有两种情形，一种是父控件没有改变子控件的props，例如父组件代码内调用setState刷新界面，此时子控件的componentWillReceiveProps也会被调用，但props没有发生变化。还有就是父控件传递过去的props是一个复杂数据类型，所以实际上是个引用，即使props发生了变化，this.props和nextProps也是相同的。

### shouldComponentUpdate(nextProps, nextState)
通过这个回调函数返回true还是false来决定是否re-render。如果不重写的话会使用源代码的默认实现。默认实现可以参考[官方文档](https://developmentarc.gitbooks.io/react-indepth/content/life_cycle/update/using_should_component_update.html)，从代码可以看出来，只要props和state有一个改变了，就会触发re-render。怎么样认为改变了怎么样认为是不变呢？ 从代码来看，首先是===强等判断，所以如果是同一个引用，那么不管内容怎么变，都认为是不变。例如

	let old = this.state;
	old.num=999;
	this.setState(old);
这样不会触发re-render。然后是比较key-value，value的比较也是===强等。举个例子

	this.state = {num:1};
	...
	this.setState({num:1});
这里虽然setState时将state变成了一个新的对象，但因为key-value完全一致，所以也不会导致re-render。如果value是复杂数据类型同理，例如

	this.state = {obj:{num:1}}
	...
	let old = this.state.obj;
	old.num = 999;
	this.setState({obj:old})
这里虽然num变了，但并不会触发re-render。

通过限制一些re-render的触发条件，可以起到优化性能的作用。

### componentWillUpdate(nextProps, nextState)
这个方法在每次re-render之前都会被调用，因为是在render之前，所以有点类似于componentWillMount，我们在这个回调里为下次render做好准备，通过this.props和this.state可以获取到当前的props和state，通过传进来的nextProps和nextState参数可以获得新的props和state。与componentWillMount不一样的是，在这里我们是可以操作UI的，但并不建议这么做，因为此时操作的是上次渲染的UI，它们有可能在下次render时就失效了。我们也不应该在这里调用setState，因为setState又会触发componentWillUpdate,这就造成了死循环，当然如果通过对nextProps或者nextState做判断是可以杜绝进入死循环的，但最好还是避免这样操作。

### componentDidUpdate(prevProps, prevState)
正如前面说的componentWillUpdate对应componentWillMount，这里componentDidUpdate就对应着componentDidMount。它在render之后被调用，在这里就可以放心的获取和操作UI了。它的参数prevProps和prevState对应着componentWillUpdate里的this.props和this.state，而这个函数里的this.props和this.state就是当前的props和state，也就是componentWillUpdate里的nextProps和nextState。子节点的回调先于父节点被调用。在这里调用setState也需要非常小心，很可能会造成无限循环，如果确实需要的话，应该配合shouldComponentUpdate加以限制。如果我们需要对UI进行交互，比如获取某个UI的尺寸位置，这里是最合适的位置。