---
title: ReactNative之listView优化方案
date: 2017-12-26 20:18:36
tags: ReactNative
---
ReactNative的ListView一直都因为性能问题饱受诟病，从源代码可以看到，它的主要问题是没有单元行重用机制，而且屏幕外的单元行不会被销毁，所以当ListView内容越来越多时，就会占用越来越多的内存，也越来越卡。针对这个问题，目前有几种解决方案。

### ListView
ListView使用时可以有一些优化方案的。首先通过initialListSize和scrollRenderAheadDistance属性指定初始时单元格数量，可以加快初始化的速度。其次通过dataSource的rowHasChanged接口可以减少单元行re-render的次数。

### FlatList
这是官方推出的解决方案，FlatList的思路是减少渲染的单元行数量，它在render时进行计算，只渲染屏幕中和缓冲区内的单元行，其余地方使用空白代替，这样不论FlatList有多少内容，实际渲染的单元行数量基本保持不变。因为有的单元行并没有渲染，当快速滑动到这个区域时，渲染是异步的，此时就会看到白屏，然后才开始显示内容。

使用FlatList时也有一些优化方案，首先是单元行组件如果使用PureComponent可以大大减少render的数量。其次实现props.getItemLayout接口可以避免临时测量每个单元行的尺寸，大大提高性能，如果能明确每个单元行的尺寸就一定要实现此接口。

initialNumToRender属性默认为10，它设定初始时渲染的单元行数量，这些单元行会常驻内存不被销毁，目的是为了scrollToTop时没有白屏。

maxToRenderPerBatch属性默认为10，它设定了在计算渲染单元行数量时每次处理的行数，这个数值如果太大可能导致渲染的单元行较多，占用内存以及增加白屏时间，如果太小了则会增加setState的次数

windowSize属性指定了屏幕外的区域渲染多少个屏幕单元(visible length)，默认是21，它也会影响初始渲染的单元行数量。假如一个android设备高度为640，减去20像素的状态栏，一个屏幕单元是620，会额外渲染20个。这个数字如果比较大，则同时渲染的单元格数量会比较多，也增加了初始化的时间，如果比较小，则会增加出现白屏的几率。

### SGListView
[SGListView](https://github.com/sghiassy/react-native-sglistview)的原理是通过onChangeVisibleRows接口，当单元行滑动到屏幕外时将渲染内容变成一个空白View，当滑动到屏幕内时变回实际内容。这样因为屏幕外的单元行都是空白view，所以优化了内存占用。 [enhancedListView](https://github.com/39otrebla/react-native-enhanced-listview)也是类似的思路，但实现有点简陋。这个解决方案也会有白屏问题，实际上只要单元行的内容变掉，重新要渲染时，因为渲染是异步的，就都会有白屏问题。

### LargeList
[LargeList](https://github.com/bolan9999/react-native-largelist)的想法是在js层实现了单元行复用。首先它和FlatList一样有白屏问题，因为渲染是异步的，在js层实现单元行复用，要求一个View渲染某些内容到真正展示出来，这段时间里屏幕就是白的。其次复用的作用是减少了创建单元行的消耗，这个消耗在整个ListView的性能消耗里并不占大头。最后使用ref持有Component引用并进行操作实际上不是RN推荐的一种处理方式，在复杂场景下很可能出问题。所以我不是很推荐使用它，实测也有不少bug。

### RealRecyclerView
[RealRecyclerView](https://github.com/droidwolf/react-native-RealRecyclerView)是封装了Android的原生控件RecyclerView，通过接口绑定同步原生view和js组件的内容。自己封装原生组件可能是难度最大的一种方案，因为有很多坑需要填，而且Android和iOS平台下风格也会不一致。但如果弄好了，就是真正实现了单元行复用的方案。像一些大厂的技术团队比如去哪儿就封装了自己的原生listView。 github上还有一个[react-native-native-listview](https://github.com/asciiman/react-native-native-listview)是同时封装了Android和iOS平台，可供参考。
