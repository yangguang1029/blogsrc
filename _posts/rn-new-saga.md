---
title: 创建一个redux saga项目的简要流程
date: 2017-08-07 20:18:36
tags: ReactNative
---

我们先新建一个RN项目

	react-native init testrn
然后安装redux
	
	cd testrn
	npm install --save redux

在动手之前确保自己已经理解了redux的概念 [redux官方中文文档](http://cn.redux.js.org/)。

现在开始写代码了，第一步我们需要设计好state的结构，我们写一个很简单的demo，页面有两个text和两个Button，点第一个button修改第一个text的文字内容，点第二个button修改第二个text的文字内容。我们将state设计为

	{
		"subState1":{"text":""},
		"subState2":{"text":""}
	}
实际项目中的state肯定不会这么简单，可能会非常庞大，这就要求结构不能太草率，因为是树状结构，所以要掌握好分级的粒度，层级太少则可能单个子state过于复杂，因为一个reducer处理一个子state，则会导致reducer函数过于繁冗。层级太多则不易梳理结构，显得混乱。

然后我们给这两个修改text的动作设定两个action

	const CHANGE1 = "change1";
	const CHANGE2 = "change2";

然后根据这个结构来写reducer

	function reducer1(state={"text":""}, action) {
		if(action.type === CHANGE1) {
			return Object.assign({}, state, {"text":"hello" + action.data});
		}
		return state;
	}
	function reducer2(state={"text":""}, action) {
		if(action.type === CHANGE2) {
			return Object.assign({}, state, {"text":"world" + action.data});
		}
		return state;
	}
	let reducer = combineReducers({"subState1":reducer1, "subState2":reducer2});
有的人在使用combineReducers时，习惯使用ES5的对象简写，例如
	
	let reducer = combineReducers({reducer1, reducer2})
这样不是很好，这样写的话，state的实际内容就是

	{
		"reducer1":{"text":""},
		"reducer2":{"text":""}
	}
我们在使用state数据时，以reducer1为key，而reducer1本身又是reducer函数的名称，一不小心就容易搞糊涂。所以我们提倡在设计state时就想好子state的key，然后在combine时用key:reducer的形式。

为了方便使用redux，我们还需要react-redux库

	npm install --save react-redux
我们使用connect这个API，来简化触发和监听action的操作。我们开始把这个页面写出来

	import {Provider, connect} from "react-redux"

	class TestRN extends Component{
		render(){
			return (<View>
				<Text>{this.props.subState1.text}</Text>
				<Text>{this.props.subState2.text}</Text>
				<Button title="btn1" onPress={()=>{
					this.props.createSagaAction1();
				}}/>
				<Button title="btn2" onPress={()=>{
					this.props.createSagaAction2();
				}}/>
			</View>)
		}
	}

	const mapStateToProps = (state, ownProps) =>{
		return state;
	}
	const mapDispatchToProps = (dispatch, ownProps)=>{
		return bindActionCreators({createSagaAction1, createSagaAction2}, dispatch);
	}
	export default connect(mapStateToProps, mapDispatchToProps)(TestRN)
这段代码里，我们点击按钮后，并不是发出了CHANGE1和CHANGE2事件，而是createSagaAction1和createSagaAction2，这是因为我打算在接下来使用redux saga，让它收到而是createSagaAction1和createSagaAction2后，模拟一次异步操作，再由saga来发出CHANGE1和CHANGE2事件

redux saga是用来处理异步操作的，所以我们先写个模拟异步的功能函数

	function delay(cb, time) {
		return new Promise((resolve)=>{
			setTimeout(()=>{
				cb(parseInt(Math.random() * 100));
				resolve();
			}, time);
		})
	}
	async function getNum(){
		let a;
		await delay((num)=>{
			a = num;
		}, 5000);
		return a;
	}
然后开始redux saga相关，首先是安装saga
	
	npm install --save redux-saga
然后开始代码，我们把点击按钮要发出的两个action实现出来然后监听并处理

	import regeneratorRuntime from "regenerator-runtime";

	const SAGA_ACTION1 = "sagaAction1";
	const SAGA_ACTION2 = "sagaAction2";
	function createSagaAction1(){
		return {"type": SAGA_ACTION1};
	}
	function createSagaAction2(){
		return {"type": SAGA_ACTION2};
	}
	function* sagaFunc1(){
		while(true) {
			yield take(SAGA_ACTION1);
			let a = yield call(getNum);
			yield put({type:CHANGE1, data:a});
		}
	}
	function* sagaFunc2(){
		while(true) {
			yield take(SAGA_ACTION2);
			let a = yield call(getNum);
			yield put({type:CHANGE2, data:a});
		}
	}
	function* mySaga(){
		yield fork(sagaFunc1);
		yield fork(sagaFunc2);
	}
这里需要注意的就是saga函数必须是generators函数，不能用async, await。 sagaFunc1通过使用三个effect来进行操作，首先使用take来监听SAGA_ACTION1，然后使用call来阻塞调用异步函数，最后使用put来发出CHANGE1这个action，这时我们前面写的reducer收到CHANGE1这个action，就会修改state，从而让页面发生变化。

然后就是不要忘了import regeneratorRuntime，否则项目是跑不起来的，会出现红屏错误，提示cannot read property 'mark' of undefined。这是babel处理generators函数所需要的。

最后是创建store和使用provider了

	let middle = createSagaMiddleware();
	const store = createStore(reducer, applyMiddleware(middle));
	middle.run(mySaga);
	
	export default class TestRNContainer extends Component{
		render(){
			return (
				<Provider store = {store}>
				<TestRN />
				</Provider>
			)
		}
	}
到此为止，一个新建项目使用redux saga就全部完成了