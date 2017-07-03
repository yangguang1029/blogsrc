---
title: ReactNative拆分bundle实践
date: 2017-07-03 20:15:36
tags: ReactNative
---

实践了一下最简单的ReactNative bundle拆分方案。将项目bundle拆分成RN源代码和业务代码，这样在热更新时不用每次都更新整个bundle。

首先新建一个项目testrn，将index.android.js内代码注释掉，只保留两行import

    import React, { Component } from 'react';
    import {
        AppRegistry,
        StyleSheet,
        Text,
        View
    } from 'react-native';

然后使用bundle命令打包成common.bundle，这就是RN源代码部分

    react-native bundle --entry-file ./index.android.js --platform android --dev false --bundle-output ./output/common.bundle

这里dev可以选择true或者false，如果为了试验建议先设成true，正式使用时使用false

然后我们将index.android.js内注释代码打开，再使用bundle命令打包成total.bundle

我们在total.bundle内搜索项目名testrn，很容易找到这么一段代码:(或者使用软件例如compareBeyond对比)

    __d(/* testrn/index.android.js */function(global, require, module, exports) {Object.defineProperty(exports, "__esModule", {
        value: true});
        var _jsxFileName = 'F:\\test\\testrn\\index.android.js';

        //中间代码省略...

        _reactNative.AppRegistry.registerComponent('testrn', function () {
        return testrn;
        });
    }, 0, null, "testrn/index.android.js");

其实这是整个的一句，从当前的\_\_d到下个\_\_d

我们把这一段放到一个新建文件叫bussiness.bundle内，同时把common.bundle的最后两行剪切到bussiness.bundle的最后

    ;require(120);
    ;require(0);

然后我们修改一下C++代码，加载bundle时改成读取common.bundle和bussiness.bundle并连接起来，就可以了。我的修改代码如下，已经测试运行正常：

    //node_modules\react-native\ReactAndroid\src\main\jni\xreact\jni\CatalystInstanceImpl.cpp
    void CatalystInstanceImpl::jniLoadScriptFromAssets(
        jni::alias_ref<JAssetManager::javaobject> assetManager, const std::string& assetURL) {
        const int kAssetsLength = 9;  // strlen("assets://");
        auto sourceURL = assetURL.substr(kAssetsLength);

        auto manager = extractAssetManager(assetManager);
        // auto script = loadScriptFromAssets(manager, "index.android.bundle");
        auto script1 = loadScriptFromAssets(manager, "common.bundle");
        auto script2 = loadScriptFromAssets(manager, "diff.js");

        auto script = folly::make_unique<JSBigBufferString>(script1->size()+script2->size());
        memcpy(script->data(), script1->c_str(), script1->size());
        memcpy(script->data() + script1->size(), script2->c_str(), script2->size());

        if (JniJSModulesUnbundle::isUnbundle(manager, sourceURL)) {instance_->loadUnbundle(
            folly::make_unique<JniJSModulesUnbundle>(manager, sourceURL),
            std::move(script),
            sourceURL);
            return;
        } else {
            instance_->loadScriptFromString(std::move(script), sourceURL);
        }
    }