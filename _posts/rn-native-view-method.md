---
title: ReactNative之原生UI导出方法
date: 2018-09-27 21:18:36
tags: ReactNative
---
在官方文档的原生UI模块章节: ([IOS](https://reactnative.cn/docs/native-components-ios/) [Android](https://reactnative.cn/docs/native-components-android/))，我们可以学会如何导出原生UI组件，如何导出prop，如何设置事件回调等等，但是缺少一个内容，那就是如何导出方法。举个例子，我们在使用ScrollView组件时，如果想让它滚动，需要先获取到它的ref，然后调用它的scrollTo方法，这就是一个原生UI导出的方法。通过阅读源代码，我找到了如何实现的方案，这里介绍一下。

### iOS
iOS端直接在继承自RCTViewManager的类中提供接口。照着下面的模板写就可以了，将获取到的view转换成实际的View然后调用方法。

```
#import <React/RCTUIManager.h>

RCT_EXPORT_METHOD(scrollToIndexWithOffset:(nonnull NSNumber *)reactTag
                  index:(NSInteger)index
                  offset:(CGFloat)offset
                  animated:(BOOL)animated)
{
    [self.bridge.uiManager addUIBlock:
     ^(__unused RCTUIManager *uiManager, NSDictionary<NSNumber *, UIView *> *viewRegistry){
         UIView *view = viewRegistry[reactTag];
         if([view class] == MyTableView.class) {
             MyTableView* table = (MyTableView*)view;
             [table scrollToIndex:index offset:offset animated:animated];
         }else {
             RCTLogError(@"tried to call scrollToIndexWithOffset on %@ "
                         "with tag #%@", view, reactTag);
         }
     }];
}
```

### Android
android端处理方式不一样，我们在继承SimpleViewManager或者ViewGroupManager的类中需要重写getCommandsMap方法，提供暴露到js层的command命令。然后重写receiveCommand方法，通过commandId判断js层是想要调用什么方法，然后把参数转换好之后进行调用。

```
@Override
    public @javax.annotation.Nullable
    Map<String, Integer> getCommandsMap() {
        return MapBuilder.of(
                "scrollToIndexWithOffset",
                COMMAND_SCROLL_TO);
    }

@Override
    public void receiveCommand(
            MyView scrollView,
            int commandId,
            @javax.annotation.Nullable ReadableArray args) {
        if(commandId == COMMAND_SCROLL_TO) {
            int index = Math.round(PixelUtil.toPixelFromDIP(args.getInt(0)));
            float offset = Math.round(PixelUtil.toPixelFromDIP(args.getDouble(1)));
            boolean animated = args.getBoolean(2);
            scrollView.scrollTo(index, offset, animated);
        }
    }
```

### javaScript

在js层调用的代码为

```
  scrollToIndexWithOffset (index, offset, animated) {
    UIManager.dispatchViewManagerCommand(
      ReactNative.findNodeHandle(this.tableRef),
      UIManager.MyTableView.Commands.scrollToIndexWithOffset,
      [index, offset, animated]
    )
  }
```
这里的tableRef就是原生组件在js层使用ref获取到的。scrollToIndexWithOffset对应着原生暴露的方法名(iOS为RCT_EXPORT_METHOD之后的方法名，Android为getCommandsMap暴露的方法名)，后面三个参数数组一次是原生方法接受的参数。

这就是原生组件封装方法到js层的全部流程了，这是基本的操作，实际开发中再注意下例如参数类型转换等小问题即可。