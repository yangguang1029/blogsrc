---
title: ReactNative之封装组件
date: 2017-12-02 20:18:36
tags: ReactNative
---
在项目开发中有时候会需要封装一些自定义组件以便复用，本文稍微整理一下。

我们基于一个自定义组件进行封装，这样方便通过console观察函数的调用情况

	class MyComponent extends Component{
		componentWillMount(){
			console.log("myComponent componentWillMount....");
		}
		componentDidMount(){
			console.log("myComponent componentDidMount....");
		}
		render(){
			return (<View>
				<Text>123</Text>
				<Text>456</Text>	
			</View>);
		}
	}
如果基于特定某种组件封装，那实际上就是继承，在render的时候，调用父类的render()即可。例如

	class HighComponent extends MyComponent{
		componentDidMount(){
			super.componentDidMount();
			console.log("HighComponent componentDidMount....");
		}
		render(){
			return(<View style={{width:100,height:100,backgroundColor:"red"}}>
        		{super.render()}
        	</View>)
		}
	}
这里需要注意一点的就是分清子类是否需要重写父类的方法，如果不重写，则会直接使用父类的实现，就像上面的componentWillMount函数。如果重写，判断是否需要使用super调用父类的实现，比如上面的componentDidMount函数。

还有一种基于特定组件封装的办法，就是重写它的render方法，例如

	import {cloneElement} from "react"
	let originText = Text;
	Text.prototype.render = function(...args){
		let text = originText.apply(this, args);
		return cloneElement(text, {style:[
			text.props.style,
			{color:"red"}	
		]})
	}
然后再使用Text，就发现字体颜色都变成红色了。这个cloneElement是react库里提供的一个方法，可以到源代码里查看了解如何使用

如果不基于特定组件，那写一个封装的函数，把需要被封装的Component传进去，例如

	 function highComponent(Com){
    	return ({children, ...props}) => {
        	return(<View style={{width:100,height:100,backgroundColor:"red"}}>
        		<Com {...props}>
            		{children}
        		</Com>
        	</View>)
    	}
	}
	const HighComponent = highComponent(MyComponent);
或者

	function highComponent(Com){
    	class Tmp extends Component{
        	render(){
            	return(<View style={{width:100,height:100,backgroundColor:"red"}}>
            		<Com {...this.props}/>
            	</View>)
        	}
    	}
    	return Tmp;
	}
	const HighComponent = highComponent(MyComponent);
这个demo很简单，不论往函数里传什么Component，都会被装在一个我们自定义的View里面。

这两个写法效果是一样的，但后者比前者更强大一点，基于类可以实现更多功能。

### 2017/12/16添加：
需要注意在封装组件时，如果有内部使用的style，应该使用this.props.style和内部的进行组合，否则在使用这个封装组件时传入的style就不起作用了，对于上面例子里的HighComponent，下面设置的style不会起作用。

	<HighComponent style={{marginLeft:50}} />
要想让传入的style生效，在封装时就要使用this.props.style

	class HighComponent extends MyComponent{
		render(){
			return(<View style={[this.props.style, {width:100,height:100,backgroundColor:"red"}]}>
        		{super.render()}
        	</View>)
		}
	}