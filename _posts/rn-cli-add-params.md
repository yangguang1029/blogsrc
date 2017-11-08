---
title: ReactNative之给bundle命令增加参数
date: 2017-11-06 20:18:36
tags: ReactNative
---

因为拆分bundle的需要，在使用react-native bundle命令打业务bundle时，需要不同bundle的module id不一样，如果直接打，它们的id都是从0开始递增的。为了解决这个问题，通过修改源代码，给react-native bundle命令增加了两个参数，指定打bundle时生成ModuleID的行为。

首先我们跟踪下react-native bundle命令运行的轨迹

cli功能的源代码位于node_modules/react-native/local-cli文件夹内，cliEntry.js的111行

	return command.func(argv, config, passedOptions);
是执行命令行的入口，react-native bundle命令就是从这里进入了local-cli/bundle/bundle.js内的bundle方法，然后进入buildBundle.js内的buildBundle方法。

之后是node_modules/react-native/packager/react-packager/src/Server/index.js。从它的buildBundle方法，可以再跟踪到packager/react-packager/src/Bundler文件夹，这里的index.js内有一个方法createModuleIdFactory就是给每个模块生成一个module id的地方，我们把这个函数改一下就可以了。

因为参数传递比较复杂，我采用了一种比较很简单而且不会修改太多源代码的方法，就是在local-cli/bundle/bundle.js的bundle方法内读取我们增加的参数，存成全局变量，在需要用的地方读取即可。

	function bundle(argv, config, args, packagerInstance) {
  		let cid = args.cid;	//modified by guangy cid为common module的最大数字 add为需要加的数字
  		let add = args.add;
  		setCidAndAdd(cid, add);

  		return bundleWithOutput(argv, config, args, undefined, packagerInstance);
	}

存储和读取cid和add参数的代码为

	let cid = 10000;
	let add = 0;

	export function setCidAndAdd(_cid, _add) {
    	cid = parseInt(_cid);
    	add = parseInt(_add);
	}

	export function getCidAndAdd(){
    	return {cid, add}
	}

最后在createModuleIdFactory方法里，通过调用getCidAndAdd获取cid和add的值来使用就可以了。

可以看到cli功能是用nodejs实现的，对于react-native bundle命令，从命令行读取什么参数，是否必带，是否有默认值等等在local-cli/bundle/bundleCommandLineArgs.js里进行配置，我们这次需要增加两个参数，只需要照已有的增加就行了。command里使用<>表示强制要求必须带这个参数。

	{ //modified by guangy 增加两个参数 add和cid
    command: '--cid <cid>',
    description: 'common的最大Module id
  	},{
    command: '--add <add>',
    description: '需要加的数字，比如10000，20000',
  	},
然后还需要修改下node_modules/react-native/packager/react-packager/src/Server/index.js文件里的const bundleOpts = declareOpts({...})
增加

	cid: {  //modified by guangy 增加两个参数
    	type: 'string',
    	required: true,
  	},
  	add: {
    	type: 'string',
    	required: true,
  	},
即可。

如果要修改其他命令，也可以照着这个思路，先把流程捋顺了，不用每行代码都看明白，大概找到需要改动的地方就行了