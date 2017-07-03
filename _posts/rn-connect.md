---
title: Redux中的Provider和connect
date: 2017-06-16 11:15:36
tags: ReactNative
---

redux里有不少概念，一时半会看不明白，这里讲下我理解的provider和connect。我们知道使用Reudx，数据作为state被存储在一个单独的store中。我们在渲染时从state获取数据，需要修改数据时，dispatch一个action即可。provider和connect的作用，是为了更方便的存取state数据。

如果不使用provider和connect，也是完全没问题的，这样的话我们需要把store传入到Component中以便使用，例如需要这么写：

	index.android.js:	//此代码缺少action和reducer的实现，并不能直接运行，只是用以描述
	
	let store = createStore(reducer);
	export default class testrn extends Component{
		render(){
			<NoConnect store={store}/>
		}
	}

	NoConnect.js:

	export default class NoConnect extends Component{
		constructor(props){
			super(props);
			this.state = this.props.store.getState();
		}
		render(){
			return (<View>
				<Text>this.state.prop1</Text>
				<Button title="click" onPress={()=>{
					this.props.store.dispatch(action);
					this.setState(this.props.store.getState());
				}}>
			</View>)
		}
	}

从上面可以看出来，我们主要是通过把store传入Component，然后利用它的getState和dispatch接口进行存取数据，数据需要保存为自身的state，在dispatch后需要通过setState来刷新界面。

如果使用provider和connect，就可以大大简化代码了。例如

	index.android.js:

	let store = createStore(reducer);
	export default class testrn extends Component{
		render(){
			<Provider store={store}>
            <TestContainer  />
            </Provider>
		}
	}

	testContainer.js:
	import { connect } from 'react-redux';
	class testContainer extends Component{
		render(){
			return (<View>
				<Text>this.props.text1</Text>
				<Button title="click" onPress={()=>{
					this.props.change1("123");
				}}>
			</View>)
		}
	}

	const mapStateToProps = (state, ownProps)=>{
		return {
			text1:state.prop1
		}
	}

	const mapDispatchToProps = {
		change1:Actions.createAction1
	}

	export default connect(mapStateToProps, mapDispatchToProps)(testContainer)

从上面代码可以看出来，在Component里不再需要使用store变量，代码简化了。只要被Provider包含着的组件及其子组件，都可以使用connect方法，就不需要到处传递store变量了。

mapStateToProps的作用，就是把state内的值转换成Component的props的值，这样在Component内使用时，不需要通过store.getState来获取并存为自己的state了。每当state发生变化时，这个方法就会被调用，这样Component的props就被修改了，于是就不用再通过setState来通知页面刷新。

mapStateToProps是一个方法，它的第一个参数就是state，第二个参数ownProps是传递给Component的props。在上述代码中就是`<TestContainer />`处传递的props

mapDispatchToProps的作用，就是把创建action的方法，绑定在Component的props上，这样就不需要通过store.dispatch来更改state。

上述代码中mapDispatchToProps是一个Object，它的values就是创建action的方法，keys绑定为Component的props属性，这样在testContainer中调用this.props.change1就创建并发布了一个action。

mapDispatchToProps也可以是一个方法，它的第一个参数是store的dispatch方法，第二个参数是ownProps。用方法实现比起用Object实现，可以做更多的注入操作，代码如下

	const mapDispatchToProps = (dispatch, ownProps) {
		return {
			change1:(data)=>{
				console.log("dispatch action1.....");
				dispatch(Actions.createAction1(data));
			}
		}
	}

可以看到如果用方法来实现，在change1里就可以做很灵活的操作了。同时Redux提供了一个很简便的接口bindActionCreators(Actions, dispatch)，使用它相当于使用Object实现，并且key和创建action的方法名一致。

上面代码里用到的Actions，是创建action的接口

除了上面提到的mapStateToProps和mapDispatchToProps外，connect方法后面还可以再带两个参数

mergeprops

options: