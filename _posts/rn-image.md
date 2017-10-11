---
title: ReactNative之Image控件从js到java的追踪流程
date: 2017-09-19 11:18:36
tags: ReactNative
---
我们以image控件为例，简单的介绍下一个系统控件的实现，方便进行自定义，以及了解它的内部实现。

我们要使用Image的话，第一步就是
	
	import {Image} from "react-native"
我们需要找到源文件export出Image的地方，它位于node_modules/react-native/Libraries/Image目录下。基本上RN的js源代码都在这个Libraries目录下。

在Image.android.js里，文件结尾是

	module.exports = Image;
证明我们使用的Image就是这里导出的。在这个文件的render函数里，可以看出来它使用了RKImage控件。然后查找RKImage的来源

	var RKImage = requireNativeComponent('RCTImageView', Image, cfg);
可以看出来，RKImage是native的实现，所以我们到node_modules/react-native/ReactAndroid/src/main/java目录下搜索关键字RCTImageView,找到在哪里注册的。

观察一下搜索结果，可以看到有两个类RCTImageViewManager和ReactImageManager，他们都是导出到js层的类，且导出名字都是RCTImageView。

我们找一下这两个类是在哪里注册的，如果对流程比较熟悉的话，看到它们继承自ViewManager也已经知道了。在node_modules\react-native\ReactAndroid\src\main\java\com\facebook\react\shell\MainReactPackage.java的createViewManagers方法里可以看到

	if(useFlatUi) {
		viewManagers.add(new RCTImageViewManager());
	}else{
		viewManagers.add(new ReactImageManager());
	}
所以根据useFlatUi的值，Image控件的native实现,可能是node\_modules\react\-native\ReactAndroid\src\main\java\com\facebook\react\views\image\ReactImageView.java或者node\_modules\react\-native\ReactAndroid\src\main\java\com\facebook\react\flat\RCTImageView.java

其余控件如果想追踪native实现，也可以按这个流程走就行了。