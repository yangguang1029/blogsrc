---
title: ReactNative之react-navigation使用
date: 2017-12-19 20:18:36
tags: ReactNative
---
react-navigation是官方推荐的导航功能库，这里稍微总结一下如何使用它进行界面切换，以及一些细节问题。详情可以查看[官方文档](https://reactnavigation.org/)

一般使用系统自带的空间StackNavigator来进行界面切换。从名字也可以很直观的看出，这个导航的类就像一个stack，push一个新的界面上来，或者pop一个界面出去，当然也可以跳转，一次pop多个界面。

### 初始化

	let Nav = StackNavigator(RouterConfigs, StackNavigatorConfig)

**RouteConfigs**是一个Object，用于注册所有可以跳转的界面。如果需要跳转的界面比较多，可以写一个脚本来生成，每个key-value形式为

	screen1: {
		screen:MyComponent,
		path:xxx,
		navigationOptions:({navigation})=>({
			title:xxx
		})
	}
screen对应Component类的名称，navigationOptions是一个回调函数，它会在每次界面被push时调用。它的参数是

	{navigation:xxx, navigationOptions:xxx, screenProps:xxx}
我们可以从这个参数中解构出navigation，获取很多有用的信息，比如传入的参数navigation.state.params等等。然后返回一个Object，这个返回的Object被称为Screen Navigation Options，它用来设置一些UI属性，比如当前界面标题文字，标题栏样式等。

**StackNavigatorConfig**是一个Object,它可以指定初始显示哪个界面，可以指定整个StackNavigator通用的样式等。例如我们希望所有的界面都不需要显示标题栏，那么在这里设置headerMode为none即可。

### 跳转
每个在RouteConfigs里注册了的screen都是一个Component类，它的props都会自动多了一个navigation属性，也就是

	this.props.navigation
通过它可以进行界面跳转，回跳，获取参数等操作。

- navigate 这是一个function，通过它来进行界面跳转。 形式为 navigate(routeName, params, action)，也就是push一个在RouteConfigs里key为routeName的界面，传递参数为params。 每次navigate一个界面都是新生成界面然后push，不会重用stack里已有界面。
- state 这是一个object, 它的内容为{routeName:xxx, key:xxx, params:{xxx}} 这里routeName就是当前界面在RouteConfigs里注册时的用的key（也就是示例中的screen1）, key则是系统自动生成的一个属性，这个key在使用goBack()函数指定跳回到某个界面时需要用到。params则是跳转时传入的参数，所以我们使用this.props.navigation.state.params来获取传入的参数。
- setParams 这是一个function，使用它改变传入的参数
- goBack 这是一个function，通过它返回到之前的界面，如果不带参数，则默认为退出当前界面回到上一层，如果参数为null，官方文档说`go back anywhere, without specifying what is getting closed`,看起来有点奇怪，不明白go back anywhere是不是任意跳转，但通过demo测试发现和不带参数表现是一样的。如果传入参数，则表示从传入参数代表的界面网上跳转一层，**注意这个参数不是RouteConfigs里的key（即screen1），而是上面state里的那个key(即this.props.navigation.state.key)**，因为只能获取当前界面的this.props.navigation.state.key，所以在A界面回跳需要B界面的key时，需要把B界面的key存起来或者传递给A。
- dispatch 这是一个function，用来发布一个action，这个接口用的不多，属于比较深入的用法，具体查看官方文档。

### 使用
上面代码里生成的Nav本身是一个Component，所以不要把它想复杂了，就当做一个普通的Component来使用就可以了。

如果把Nav传给AppRegistry.registerComponent来作为起始Component。那很简单，在RouteConfigs里注册的各个界面里使用this.props.navigation进行操作就可以了。

如果作为一个普通Component使用，它的父容器内其它component想要进行navigator跳转，则通过它的ref来进行操作。例如

	render(){
		return <View>
			<Button onPress={()=>{
				this._ref && this._ref.dispatch(
      				NavigationActions.navigate({ routeName: someRouteName })
    			);
			}}/>
			<Nav ref={(c)=>this._ref=c}/>
		</View>
	}

其它例如TabNavigator，DrawerNavigator的使用，大体和StackNavigator类似。其它高端的操作例如自定义Navigator,自定义Route等都参考官方文档。

### 回跳多个界面的解决方案
老版本的navigator可以通过routes列表获取当前的界面栈，也有popToRoute(),popToTop()这样的接口可以直接跳转。而react-navigation则没有界面栈的信息，只能通过goBack()传入一个key来指定跳转，这个key还只能获取到当前所在界面的，没法获取其他界面的key。如果要回跳多个界面，一个解决方案就是在需要回跳的目标界面获取key，通过props一路传递下来，然后在跳转界面使用。例如

	//A.js
	toB(){
		let key = this.props.navigation.state.key;
		this.props.navigation.navigate("B", {returnKey:key});	
	}
	//B.js
	toC(){
		this.props.navigation.navigate("C", 
		{returnKey：this.props.navigation.state.params.returnKey});
	}
	//C.js
	back(){
		this.props.navigation.goBack(this.props.navigation.state.params.returnKey)
	}
这里从A传入key，在C界面跳转，注意并不是跳转到A界面，而是从A界面离开，调到A之前的一个界面。如果不通过传递的话，也可以把key存成全局变量，这样可以比较简单的实现回跳多个界面。还有一种hack的手段，就是获取navigation的ref，然后操作它的私有成员属性或者方法，来获取到调用栈信息进行跳转，最好还是避免使用这种方法吧。