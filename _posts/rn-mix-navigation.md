---
title: ReactNative之混合Navigation跳转问题
date: 2018-01-12 20:18:36
tags: ReactNative
---
首先把界面列出来

	class Tab1 extends Component{
		render(){
			return <View><Text>tab1</Text>
					<Button title="totab2" onPress={
						()=>{this.props.navigation.navigate("tab2")}
					}/>
					<Button title="toscene2" onPress={
						()=>{this.props.navigation.navigate("scene2")}
					}/>
		}
	}
	class Tab2 extends Component{
		render(){
			return <View><Text>tab2</Text>
					<Button title="totab1" onPress={
						()=>{this.props.navigation.navigate("tab1")}
					}/>
					<Button title="toscene2" onPress={
						()=>{this.props.navigation.navigate("scene2")}
					}/>
		}
	}
	const TabNav = TabNavigator({
		tab1：{screen:Tab1,}
		tab2：{screen:Tab2,}
	}})
	class Scene2 extends Component{
		render(){
			return <View><Text>scene2</Text>
					<Button title="toscene1" onPress={
						()=>{this.props.navigation.navigate("scene1")}
					}/>
		}
	}
	const StackNav=StackNavigator({
		scene1:{screen:TabNav},
		scene2:{screen:Scene2}
	})
这是最简单的情况，一个StackNavigator内的界面是TabNavigator，在Tab1和Tab2里，不论是进行TabNavigator还是StackNavigator内的跳转，都直接使用this.props.navigation.navigate即可。在注册生成TabNavigator和StackNavigator时给每个界面都注册了一个唯一的key，根据这个key可以在任意界面间跳转，例如在scene2界面，除了可以跳回scene1外，也可以指定跳回tab1或者tab2。

如果TabNavigator被包装在一个普通Component内，情况就稍微复杂一些，例如

	class TabContainer extends Component{
		render(){
        	return <View style={{flex:1}}>
            	<Text style={{margin:20}}>tabContainer</Text>
            	<TabNav />
        	</View>
    	}
	}
	const StackNav=StackNavigator({
		scene1:{screen:TabContainer},
		scene2:{screen:Scene2}
	})
直接运行的话就会发现,在Tab1和Tab2界面之间的跳转没问题，但没法跳转到scene2了，解决方案是将\<TabNav />替换成

	<TabNav navigation={this.props.navigation}/>
然后添加一行

	TabContainer.router = TabNav.router;
就和上面行为一样了，可以在各个界面自由跳转。上面这句话通过给TabContainer增加一个router属性，将一个普通Component变成一个navigator，所以就能跳转了。

还有一种办法是通过给TabNav设置screenProps的办法把this.props.navigation传到Tab1和Tab2里面去，代码就是

	<TabNav screenProps={{navigation:this.props.navigation}}/>
在Tab1和Tab2里跳转到Scene2就可以

	this.props.screenProps.navigation.navigate("scene2")

使用这个方案，在Scene2界面只能往StackNavigator的界面跳，不能像第一种方案一样直接跳到tab1或者tab2，所以不够灵活，推荐使用前一种方案。