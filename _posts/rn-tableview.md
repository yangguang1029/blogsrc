---
title: ReactNative之封装TableView组件
date: 2018-05-22 20:18:36
tags: ReactNative
---
众所周知，ReactNative中的列表组件，不论是老版的ListView还是新版的FlatList，都不是对原生列表的封装，只是在JavaScript层在ScrollView的基础上实现的，如果能基于原生列表组件进行封装，就真正实现了单元行的复用，最近尝试了下对iOS平台tableView的封装，demo已经运行正常了，这里把思路整理一下。

封装tableView本身很简单，按[官方教程](https://reactnative.cn/docs/0.51/native-component-ios.html#content)走就行了。我们从js中传一个rowCount属性过来，用于给tableView的numberOfRowsInSection回调使用。对tableView来说，最重要的就是每个tableViewCell怎么渲染了。因为每个单元行渲染的内容需要从js端传过来，如果能够在原生层捕获到这个js中渲染的组件，然后放到每个TableViewCell里去作为它的subview，当这个TableViewCell被重用时，获取到这个subview，然后通知js端刷新这个组件的内容即可。

从原生捕获js组件的方案就是，在js层的tableView里，给它添加子控件，然后在对应的原生tableview代码中，通过

    - (void)insertReactSubview:(UIView *)subview atIndex:(NSInteger)atIndex {
  
    }
接口，可以获取到这个子控件。这些控件既然需要从原生层往js层发消息，那么理所当然也需要是原生封装的组件了，我们给它通过RCTBubblingEventBlock回调，就可以让它往js发消息了，这样当一个tableViewCell被重用时，我们已经知道它被重用到了哪个位置，把这个位置发到js层，js层刷新显示即可。

在js层使用的时候，我们需要往tableView里添加子控件用于显示单元行内容，这些子控件在每次tableViewCell新建的时候都需要一个，所以理论上来说，这些子控件的数量应该保证至少能填满一个tableView的空间，像demo里tableview的高度是300，单元行高度是40，那么至少需要8个。但如果只放8个，就会发现在快速滑动时不够用了，导致可能个别单元行变成了空白。推测是快速滑动时，部分tableViewCell还没来得及进入回收队列，所以需要新建，所以在demo里我就放了两屏的数量，也就是16个，就没有再出现问题了。

以上就是实现思路，具体代码可以查看[demo](https://github.com/yangguang1029/MyReactNative/tree/master/tableview)