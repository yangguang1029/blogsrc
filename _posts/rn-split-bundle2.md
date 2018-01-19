---
title: ReactNative拆分bundle方案
date: 2017-11-03 20:15:36
tags: ReactNative
---
### 为什么要拆分bundle？

我们知道RN项目中的js代码会被打成一整个bundle来加载执行，这个Bundle包含了我们自己写的业务代码和RN源代码。如果不进行拆分，我们在做热更新时，哪怕业务代码只更改了一行，也需要更新一整个bundle，其中RN源代码至少占用500k以上，如果使用了第三方库如redux等还会更多，这是很大的浪费。其次是可能一个项目中包含多个RN业务，这样加载它们各自的bundle都带有RN源代码以及第三方库，也就意味着这些公共代码被重复加载了很多次。

### bundle内容

我们使用命令来打一个bundle进行观察，看bundle内都有什么

	react-native bundle --entry-file index.android.js --platform android --dev false --bundle-output android/app/src/main/assets --assets-dest android/app/src/main/res

这里我们生成的是release版本的bundle，比较容易看出来三个部分。如果需要阅读代码，则把--dev设为true生成debug版本的bundle即可

第一个部分在release版本的bundle内大概占11行，他们是为js解释器注入了一些关键字和功能

	global.require=_require
	global.__d = define
	var ErrorUtils = ...
	Object.assign = ...
	function guardedLoadModule(moduleId, module){	...

第二个部分占了整个bundle的绝大部分内容，它们都是以\_\_d开头，我们以一个最短的举例

	__d(function(t,n,c,i){"use strict";function o(t,n,c,i,o){}c.exports=o},22);

第三个部分是模块的调用，第二个部分是进行了模块的注册，如果想要代码执行，就必须调用模块，这是bundle内的最后两行

	;require(65);
	;require(0);
这个数字65根据不同的项目是不一样的。

### 如何拆分

bundle需要被拆分为RN源代码和业务代码。我们知道js代码的入口在index.android.js(或者index.ios.js)，从这个入口文件起根据依赖关系，最后所有引用到的js文件被合并成了一整个bundle，我们给它命名total.bundle。然后我们把index.android.js里的代码注释掉，只保留对RN源代码的引用，例如

	import "react"
	import "react-native"

当然如果我们把一些第三方库例如redux也算入RN代码的话，也可以加上。这样生成的bundle我们命名为common.bundle。

我们观察一下common.bundle里第二部分定义的最后一个模块数字id为多少，在total.bundle内，从这个id以后的内容我们就可以拆分出来，生成新文件business.bundle，这就是我们的业务代码了。

然后我们处理一下common.bundle，我们找到它第二部分里定义模块0的那行代码和最后一行也就是require(0)去掉，这是入口文件，我们common bundle只需要引擎。而且我们的业务代码中入口文件也被定义为模块0，如果有两个模块0，则在分步加载时会有问题。

这样我们就把原来的total.bundle拆分成了common.bundle和business.bundle，之后就是如何使用了

### 合并加载

最简单的方案就是在加载bundle的时候，将这两个bundle一起读成字符串，然后合并成一个字符串，再进行加载。

我们可以在node_modules/react-native/ReactCommon/Instance.cpp里找到加载bundle的方法：loadScriptFromFile，在这里进行拼接即可。

这种方案可以减少热更新时bundle的大小，但不能优化加载bundle时的内存使用。

### 分步加载

这种方案需要对RN加载bundle的流程比较熟悉。我们在加载common.bundle时，不需要进入RN界面，也就是不需要启动一个ReactNativeActivity，而在源代码中，是在ReactNativeActivity的onCreate函数里加载js bundle并创建context的，所以我们将这些操作提出来。然后当需要加载业务代码business.bundle时，也不能简单的使用一个ReactNativeActivity，因为我们需要使用之前创建好的context，而不能重新创建。

具体操作是：我们使用一个Application implements ReactApplication，它会持有一个ReactNativeHost对象，这个对象host对象又会持有ReactInstanceManager对象，我们调用这个manager对象的createContextInBackground方法来加载common.bundle，创建了js context。

当我们需要加载business.bundle并进去RN界面时，我们使用一个普通的Activity，在它的onCreate函数里，构造一个ReactRootView,并设为contentView, 然后我们通过Application获取到host再获取到ReactInstanceManager，通过反射或者修改源代码，将manager绑定给这个ReactRootView，通过给它设置jsModuleName, 最后通过ReactInstanceManager获取CatalystInstance类，调用其loadScriptFromAssets或者loadScriptFromFile接口加载business.bundle即可。

这种方案将原来一整个Bundle加载分成了两步，在加载business.bundle时能够减少内存使用，提高加载性能。

### 结束

我在github上放了一个[demo](https://github.com/yangguang1029/ReactNativeSplit.git)。做到让这个demo运行的程度并不意味着就万事大吉了，多个bundle之间模块的冲突，全局变量和方法冲突，图片路径问题，sourcemap解析等还有很多需要处理的问题，我们解决了不少，且目前已经在线上使用了。欢迎讨论交流。