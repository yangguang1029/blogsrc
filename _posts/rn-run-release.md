---
title: ReactNative之生成android debug安装包
date: 2017-11-02 20:18:36
tags: ReactNative
---
我们使用react-native init创建一个空的项目，想要让它在android设备上跑起来，[官网教程](https://reactnative.cn/docs/0.43/running-on-device-android.html#content)给的方案就是使用react-native run-android命令开启联网调试，或者使用./gradlew assembleRelease来生成安装包。 前者必须依赖开发机开启联网服务，然后手机设置好服务器和端口并连接，否则要么屏幕一片空白，要么提示红屏报错。找到android/app/build/output/appDebug.apk可以看到安装包内没有Bundle等资源。后者需要配置签名。实际上如果我们想查看apk实际运行状况，可以很快生成一个debug安装包。

### 打包bundle
这是最重要的一步，在项目根目录下执行
	
	react-native bundle --entry-file index.android.js --platform android --dev false --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res

这里最重要的是指定--bundle-output和--assets-dest两个参数。首先是--bundle-output，它必须放在android/app/src/main/assets目录下，如果该目录不存在就创建。必须指定文件名为index.android.bundle。 所有的图片资源必须放在android/app/src/main/res下，否则会无法找到图片资源而不能显示。

### 安装运行

到android目录下执行./gradlew installDebug即可

### tips
在打包bundle那一步中，很多参数只是遵循默认的设置，比如bundle文件名叫index.android.bundle，位置在assets目录下，这些都可以按自己的需求来改，但前提是在java代码内也要做相应的调整，如果对这块不是很熟悉就按默认的来就行了。

不过--assets-dest目录必须在res目录下这个一定要遵守，因为Android系统要使用安装包内的资源，必须先转换成res id，如果放到别的文件夹下，没法转换，最后肯定找不到资源，也就没法显示图片了。

