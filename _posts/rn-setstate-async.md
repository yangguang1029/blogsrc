---
title: ReactNative之setState的同异步
date: 2017-12-06 20:18:36
tags: ReactNative
---
在[官方文档](https://reactjs.org/docs/react-component.html#setstate)中关于setState有一段说明

> Think of setState() as a request rather than an immediate command to update the component. For better perceived performance, React may delay it, and then update several components in a single pass. React does not guarantee that the state changes are applied immediately.
> 
> setState() does not always immediately update the component. It may batch or defer the update until later. This makes reading this.state right after calling setState() a potential pitfall. Instead, use componentDidUpdate or a setState callback (setState(updater, callback)), either of which are guaranteed to fire after the update has been applied. 

可以明确地看到，setState只是发起一个请求，要求改变state，并**不一定**会立即执行。如果在setState后立即获取state，**有可能**得到的还是赋值前的旧值。这里需要特别注意的是“不一定”和“有可能”，也就意味着有的情况下是异步执行的，有的情况下是同步。我们需要搞明白分别什么情况下会是同异步。看下面的例子

    constructor(props){
    	super(props);
    	this.state={
    		text:"123"
    	}
    }
    
    componentWillUpdate(){
    	console.log("guangy componentWillUpdate")
    }
    
    _onClick(){
    	console.log("guangy before set state,now value " + this.state.text);
    	let num = Math.floor(Math.random()*100);
    	this.setState({text: ""+num });
    	console.log("guangy after set state,now value " + this.state.text);
    }
    
    render(){
    	console.log("guangy render.....")
    	return(<View>
    		<Text>{this.state.text}</Text>
    		<Button title="A" onPress={
    			()=>{
    				this._onClick();
    			}
    		}/>
    		<Button title="B" onPress={
    			()=>{
       				setTimeout(()=>{
    					this._onClick();
       				}, 10);
    			}
    		}/>
    	</View>);
    }
当点击A按钮时，输出log为

	guangy before set state,now value 123
	guangy after set state,now value 123
	guangy componentWillUpdate
	guangy render.....
可以看到这里setState是异步执行了。

当点击B按钮时，输出log为

	guangy before set state,now value 123
	guangy componentWillUpdate
	guangy render.....
	guangy after set state,now value 80
很明显，这里setState是同步执行了。

除了setTimeout外，在DeviceEventEmitter的回调函数里，也是同步执行。这跟js的事件循环机制有关，render函数,setTimeout和DeviceEventEmitter的回调都是在事件循环结束时调用，所以此时调用setState触发render会是同步的，其余时候调用setState则是异步的。

在setState为异步时，要注意如果在一次事件循环中多次setState，后面的会覆盖掉前面的，因为这一次循环里所有的setState会集中到一次来处理。 然后就是注意不要在setState后立即获取state，如果想要获取新的state，应该在setState传入回调函数作为第二个参数，在这个回调函数里获取。

setState还有一种形式就是接受function作为第一个参数，形式为

	this.setState((prevState, props)=>{
		return {xxx};
	})
这样可以明确知道当前state是什么状态，然后返回新的state。