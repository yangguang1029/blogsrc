---
title: ReactNative之一次FlatList无法局部刷新的bug修复
date: 2018-01-06 19:15:36
tags: ReactNative
---
今天发现项目中一个奇怪的问题，在使用FlatList时，每个单元行Component明明实现了shouldComponentUpdate,但是当增加一行时，还是所有的单元行都重新render了，最后找到了原因。代码中FlatList实现的keyExtractor非常简单，因为每个单元行数据的key要求是唯一的，所以直接使用了index返回

	  _keyExtractor(item, index){
        return ""+index;
    }
然后在增加数据时，又是把数据插到了数组的最前面

	let data = this.state.data;
	this.setState({data:[{num:key,key}].concat(data)})
这样就出问题了，对FlatList内的每个单元行组件CellRenderer来说，它的props包括keyExtractor给出的key和data给出的数据，假设原来数据是[0,1,2,3]，那么FlatList内的组件就包括

	<CellRenderer key="0", num=0 />
	<CellRenderer key="1", num=1 />
	<CellRenderer key="2", num=2 />
	<CellRenderer key="3", num=3 />
在数组最前面加上一个数据101后，FlatList内的组件就变成了

	<CellRenderer key="0", num=101 />
	<CellRenderer key="1", num=0 />
	<CellRenderer key="2", num=1 />
	<CellRenderer key="3", num=2 />
	<CellRenderer key="4", num=3 />
我们在单元行组件里的shouldComponentUpdate实现是：

	shouldComponentUpdate(nextProps){
        return this.props.num !== nextProps.num;
    }
所以很显然已有的4个CellRenderer因为num变化，就全部刷新了。

找到原因后，要解决就很简单了

	_keyExtractor(item, index){
        return item.num;;
    }
所以结论就是：**keyExtractor应该根据实际情况根据item数据来设置，不要贪图简单直接使用index**

最后做了下验证，keyExtractor使用index时，将数据加在数组最后，而不是插在最前，那么没问题，不会全部刷新，因为前面CellRenderer的props都没有变化。但实际项目中不要贪图省事，之所以FlatList提供这个接口让开发者去实现，就肯定有这个需要，随便返回一个index可能就把自己给坑了。

关于re-render的原理，官方有一篇文章叫[reconciliation](https://reactjs.org/docs/reconciliation.html)讲的很清楚，看完就更容易理解这个问题的本质了。
	