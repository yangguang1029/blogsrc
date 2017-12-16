---
title: ReactNative之使用LayoutAnimation创建动画
date: 2017-12-16 20:18:36
tags: ReactNative
---

LayoutAnimation是官方提供的一个实现动画的API，但官方文档比较简单，结合查看源代码和demo试验，总结了一下如何使用。

最开始重点强调一下，android平台要使用的话，必须加上这段代码才行，否则像我一样用android设备调试，写了半天发现都不起作用。

	var UIManager = require('UIManager');
	UIManager.setLayoutAnimationEnabledExperimental && UIManager.setLayoutAnimationEnabledExperimental(true);
使用LayoutAnimation实现动画其实很简单，就是在setState之前调用LayoutAnimation.configureNext，然后在下次渲染时就根据新的state产生动画了，所以先写一个最简单的例子

	class TestLayoutAnimation extends Component{
		
		constructor(props) {
			super(props);
			this.state = {left:100,top:100,width:100,height:100,isVisible:true}
		}	
		render(){
			return <View>
				<Button title="click" onPress={this._onClick.bind(this)}/>
				{
				this.state.isVisible ? 
				<View style={{position:"absolute", left:this.state.left, top:this.state.top,
					width:this.state.width, height:this.state.height, backgroundColor:"red",
				}}/>
				 : null
				}
			</View>
		}
		_onClick(){
        	LayoutAnimation.configureNext({
            	duration:500,
            	update:{
                	type:LayoutAnimation.Types.spring
            	}
        	});
        	this.setState({left:this.state.left+50,top:this.state.top+50,
			width:this.state.width+50,height:this.state.height+50});
    	}
	}
运行这个简单的demo就可以看到动画效果，就是由LayoutAnimation.configureNext产生的，我们可以通过看源代码知道这个API的使用规则。LayoutAnimation.js位于react-native\Libraries\LayoutAnimation\文件夹内，Java代码位于react-native\ReactAndroid\src\main\java\com\facebook\react\uimanager\layoutanimation文件夹内

configureNext方法接受的参数是一个Config对象，这个对象的规则是

	type Config = {
  		duration: number,
  		create?: Anim,
  		update?: Anim,
  		delete?: Anim,
	};
duration参数是必须的，指定这个动画的执行时间。 create,update,delete三个参数是Anim类型，都是可选参数。

- create指定了一个View从不可见变成可见状态时执行的动画效果，这里的不可见，包括width,height为0，或者像demo通过this.state.isVisible控制了不渲染，不包括透明度为0的情况。如果没有create参数，那view出现时是没有动画效果的
- update参数指定了View在可见状态时因为state变化产生的动画效果
- delete和create相反，当一个View变为不可见时，指定其动画效果。

所以如果一个View在执行动画前是不可见的状态，则必须配置create参数，否则配置update参数就可以。如果消失时需要动画，则配置delete参数。

我们看Anim的格式要求

	const animType = PropTypes.shape({
  		duration: PropTypes.number,
  		delay: PropTypes.number,
  		springDamping: PropTypes.number,
  		initialVelocity: PropTypes.number,
  		type: PropTypes.oneOf(Object.keys(Types)).isRequired,
  		property: PropTypes.oneOf(
    		// Only applies to create/delete
    		Object.keys(Properties),
  		),
	});
其中type参数是一定需要的，而property参数则只在create和delete时需要。简单点的话，就只看type和property参数

- type参数必须是LayoutAnimation.Types这个Enum中的值，可取的值有spring, linear, easeInEaseOut, easeIn, easeOut, keyboard 它们的具体效果可以自行通过demo测试
- property必须是LayoutAnimation.Properties这个Enum中的值，可取的值只有两个opacity, scaleXY。不看源代码大概也能推测出它的意义就是View在出现或者消失时，是按scale还是opacity的效果来。

了解这些之后我们就可以实现改变View的尺寸，坐标的动画了，但**对透明度，Transform的变动不会有动画效果**。

LayoutAnimation提供了一个接口Create方法，可以生成configureNext方法需要的参数Config

	function create(duration: number, type, creationProp): Config {
  		return {
   			duration,
    		create: {type,property: creationProp,},
    		update: {type,},
    		delete: {type,property: creationProp,},
  		};
	}
使用这个方法可以生成了一个比较简单的config，它把create,update,delete都实现了，属性只有type和property。

此外LayoutAnimation还提供了3个写好的动画效果可以直接使用，它们是LayoutAnimation.easeInEaseOut, LayoutAnimation.linear, LayoutAnimation.spring,看源代码就很容易明白，它们其实就是写好了代码实现的configureNext方法，所以使用起来就是在setState之前直接调用即可

	LayoutAnimation.easeInEaseOut();
	LayoutAnimation.linear();
	LayoutAnimation.spring();

LayoutAnimation的底层实现是在native层，所以不会被js线程卡顿影响，比较适合做一些简单的动画，使用起来也很简单。