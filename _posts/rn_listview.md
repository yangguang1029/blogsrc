---
title: ReactNative中的listView使用介绍
date: 2017-10-11 19:15:36
tags: ReactNative
---
今天下午稍微把listView的js代码看了一遍，大致总结一下它的接口和使用，[官方文档](https://reactnative.cn/docs/0.43/using-a-listview.html#content)上的介绍太过简单。listView的js源代码位于node_modules\react-native\Libraries文件夹内。

一个最简单的listView，代码如下

	<ListView
          dataSource={this.state.dataSource}
          renderRow={(rowData) => <Text>{rowData}</Text>}
     />

### dataSource

dataSource顾名思义是为了给listView提供数据源，这个类的源代码为ListViewDataSource.js。这个类除了存储数据外，还提供了4个接口给listView调用，这4个接口我们都可以自定义实现，其中2个有默认实现，2个没有。这段源代码就是

	this._rowHasChanged = params.rowHasChanged;
    this._getRowData = params.getRowData || defaultGetRowData;
    this._sectionHeaderHasChanged = params.sectionHeaderHasChanged;
    this._getSectionHeaderData =
      params.getSectionHeaderData || defaultGetSectionHeaderData;

rowHasChanged是一定要实现的，用来区分两个row是否相同，如果没有特殊需求的话，使用下面的就可以了
	
	rowHasChanged: (r1, r2) => r1 !== r2
sectionHeaderHasChanged是如果listView有分节，则必须要的，没有特殊需求的话可以直接

	sectionHeaderHasChanged: (s1, s2) => s1 !== s2
getRowData这个源代码有提供默认的实现，它用来获取每行的需要显示的数据，没有特殊需求的话不用实现
getSectionHeaderData源代码也有默认实现，顾名思义它用来获取每节的数据。

dataSource要拿来使用，除了实现必须的接口之外，还需要给它提供数据，这就用到了cloneWithRows和cloneWithRowsAndSections这两个方法，前者是后者的简化版，所以我们就拿最复杂的来举例说明。cloneWithRowsAndSections的函数声明为

	 cloneWithRowsAndSections(
      dataBlob: any,
      sectionIdentities: ?Array<string>,
      rowIdentities: ?Array<Array<string>>): ListViewDataSource
它接受三个参数，并返回一个ListViewDataSource的实例对象。第一个参数dataBlob是传入的数据，它应该是一个Object，第二个参数是一个数组，它指定了一些key，也就是说dataBlob这个Object里，sectionIdentities里的keys对应的value才是需要显示的。rowIdentities则是一个二维数组，它指定了每节的数据中，哪些key对应的数据需要显示。前面我们说过，需要显示的数据是由getRowData和getSectionHeaderData来获取的，所以上面所说的是系统默认的实现，我们当然也可以自己去实现这两个接口，来自定义数据的获取行为。 以下是一段示例代码
	
	let data=[["1","2", "3"],["4","5", "6"],["7","8", "9"]];
	const ds = new ListView.DataSource({
		rowHasChanged: (r1, r2) => r1 !== r2, 
		sectionHeaderHasChanged: (s1, s2) => s1 !== s2
	});
	<ListView
    	dataSource={ds.cloneWithRowsAndSections(data, ["0", "2"], [[0,1], [1,2]])}
	/>
这段代码的行为是显示两个section，第一个section显示1和2，第二个section会显示8和9。这个例子里dataBlob是一个数组，它只是比较特殊的Object，key是0123...，如果是普通的key-value也是一样处理。cloneWithRows同理但更为简单，它只有两个参数，第一个参数dataBlob是传入的数据，第二个参数是一个数组，指定需要显示的rowIdentities。

对于这样一段代码

	let data = ["111", "222", "333"]
	<ListView
    	dataSource={ds.cloneWithRowsAndSections(data)}
	/>
显示效果会是有三个section，每个section有3个row，这是由于系统默认的getRowData和getSectionHeaderData实现方式决定的，思考一下就能明白了。

### ListView

把dataSource弄明白之后，接下来看listView。从源代码的propTypes可以查看它能接收的props。

- dataSource就是我们上面说到的，给它传递一个dataSource实例即可

- renderSeparator函数声明为(sectionID, rowID, adjacentRowHighlighted) => renderable
这个函数可以不用实现，系统会有默认实现，它的作用是绘制listView里每节中各个行的分割线。adjacentRowHighlighted为bool值，它的值由renderRow函数指定。

- renderRow函数声明为(rowData, sectionID, rowID, highlightRow) => renderable，这是必须实现的，作用是绘制每个单元行，rowData就是从dataSource里获取来的数据，sectionID为所在节id，rowID为所在行的id。这三个数据都是dataSource传递过来的，所以像上面的那个dataSource例子，sectionID分别是"0", "1", "2", rowID是0, 1, 2。最后的highlightRow参数是一个function，它可以在renderRow函数里适当的时候调用（比如按钮被点击），调用highlightRow(sectionID, rowID)可以让这个单元在上面的renderSeparator函数里接受到的adjacentRowHighlighted变为true。不要直接在renderRow函数里调用highlightRow函数，它会导致死循环然后调用栈溢出

- renderSectionHeader函数声明为(sectionData, sectionID) => renderable，如果listView有分节，则实现此函数来绘制每节的头部，返回null或者undefined则不会渲染。

- initialListSize用来指定起始时渲染多少个单元行，如果不指定的话，系统默认是10个。但首次渲染的单元行数量不完全取决于此，还取决于一个属性值DEFAULT_SCROLL_RENDER_AHEAD = 1000，这代表整个listView最多渲染多少个逻辑像素高，首次渲染的单元行数量取这两者中较大的那个。这是用来做性能优化的，如果确实碰到性能瓶颈时，需要将源代码完全看明白才能着手，所以建议在没完全看明白源代码之前没必要去碰这些参数。

- scrollRenderAheadDistance这是一个数字，前面说过了，它参与限制首次渲染的单元行数量，默认值为1000，我们写一个demo，设置数据量比较大，然后让这个值为不同的值，可以看到首次渲染的单元行数量会不一样

- onEndReached在整个listView滚动到最底部时会被调用的回调

- onEndReachedThreshold是一个数字，指定当滑动了多少距离时会触发onEndReached事件

- pageSize指定了每次事件循环时渲染的单元格数量

- renderFooter和renderHeader函数声明为() => renderable，它们渲染整个listView的头部和底部，头部和底部会随着listView滑动。

- renderScrollComponent函数声明为(props) => renderable，用来渲染装listView内容的容器，默认实现是直接返回了一个ScrollView

- onChangeVisibleRows函数声明为(visibleRows, changedRows) => void，它在当前正在显示哪些单元行发生变化时被调用，visibleRows是一个字典，形式为{ sectionID: { rowID: true }}，表示所有当前可见的单元行，changedRows也是一个字典，形式为{ sectionID: { rowID: true | false }}，表示visible发生了变化的单元行

- removeClippedSubviews 这是一个bool值，默认是true，用来优化数据量很大时的显示性能

- stickyHeaderIndices,这是一个数字数组，用来指定哪些单元行在listview滑动时固定在屏幕顶端，只在ios平台而且是竖直方向的listView上才生效

- enableEmptySections,这是一个Bool值，用来指定当一个没有数据的节是否需要展示，例如dataSource数据为[[1,2],[],[3,4]]时，中间的那个节（包括sectionHead和rows）是否会展示，如果不指定的话这个值为undefined，就不会显示。

以上就是listView的所有props了，也就是说明白了上面的内容，使用listView来完成功能肯定没问题了，但如果希望了解更多的细节，还是需要查看源代码，包括js端以及native端的源码。react-native的最新版本提供了flatList组件，它是listView的升级版，应该优先考虑使用flatList。

ps：当我们修改listView的数据源时，即使只是修改数组内的一项，也会导致整个listView都重新刷新，如果短时间内频繁更新数据源的话，可能导致性能瓶颈，应该优化为缓存数据后集中更新一次。