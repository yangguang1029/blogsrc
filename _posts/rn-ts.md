---
title: ReactNative之在项目中使用TypeScript
date: 2017-12-27 20:18:36
tags: ReactNative
---
最近在网上找到个开源的控件，但是源代码是用TypeScript实现的，放到项目里无法直接使用，于是google了一下怎么在ReactNative项目内使用TypeScript，然后找到了一个很简单的解决方案，试了一下没有问题。

首先安装react-native-typescript-transformer模块

	yarn add --dev react-native-typescript-transformer typescript

然后在项目的根目录下创建一个文件 rn-cli.config.js

	module.exports = {  
  		getTransformModulePath() {
    		return require.resolve('react-native-typescript-transformer')
  		},
  		getSourceExts() {
    		return ['ts', 'tsx'];
  		}
	}

在项目根目录下创建一个文件tsconfig.json
	
	{
  		"compilerOptions": {
    		"target": "es2015",
    		"module": "es2015",
    		"jsx": "react-native",
    		"moduleResolution": "node",
    		"allowSyntheticDefaultImports": true
  		}
	}

然后就可以放心在项目里写TypeScript代码了，例如项目中ts目录下有test.ts文件，我们在import这个文件时，就像import一个js文件就可以了

	import './ts/test'

这些以ts,tsx为后缀的TypeScript代码文件会被转换成js文件，我们实际import的是转换后的js文件。
	