---
title: ReactNative之flatlist性能优化
date: 2018-12-20 21:15:36
tags: ReactNative
---
列表页是RN应用开发中非常常见的场景，如果单元行数量较多，单元行UI比较复杂，页面刷新比较频繁，很容易产生性能问题。本文将总结在使用flatlist组件过程中进行性能优化的方向

### 减少组件本身的刷新

首先我们需要知道，一旦flatlist刷新，它的所有renderItem就会被调用到，如果列表元素很多而且复杂，将会带来很大的性能损耗，所以我们第一件事就是避免flatlist组件本身不必要的刷新，这和所有组件避免重复刷新的做法是一样的，就是避免在props中使用临时成员变量。FlatList本身是继承自pureComponent，所以只要props或state进行浅比较不一致，就会刷新。例如下面的代码

    <FlatList
      {...this.props}
      style={{width:100,height:100}}
      data = {this.state.data}
      extraData={this.extraData}
      keyExtractor={(item,index) => '' + index}
      renderItem={this.renderItem}
      ListFooterComponent={<View style={{width:100,height:20,backgroundColor:'red'}} />}
      onScroll={this.props.onScroll}
    />
这段代码里就有很多使用不当的地方，首先是我发现很多人喜欢图方便使用{...this.props}，这是非常不合适的，不论在任何地方都要避免使用这种方式，因为把父组件的所有props原封不动拿来用，很难控制这个组件本身的props变化，从而产生不必要的刷新。onScroll和{...this.props}是一样，使用了其它地方传递来的props，尽量避免这样使用，一定要这么写的话，就去源头查看是否是临时变量，是否在每次render时都会发生变化。其次是style，keyExtractor以及ListFooterComponent，它们的本质都一样，就是使用了临时变量做props，这会导致只要父组件刷新，FlatList也必然刷新，而我们需要的绝不是这样，一个没有多余刷新的FlatList应该是只有data和extraData发生变化时才会进行刷新。改进的办法就是使用类成员变量或者类成员方法来作props，避免每次刷新时都是生成一个新的临时对象。

### keyExtractor

然后一个很重要的就是keyExtractor，FlatList的原理是往一个ScrollView里面放上所有的单元行组件作为子组件，如果了解React中的[Reconciliation](https://reactjs.org/docs/reconciliation.html)就知道，兄弟组件之间需要使用一个唯一的key来标记自身，keyExtractor就是给每个单元行一个唯一的标识，这里直接用index做标识的话，一旦列表顺序发生变化，例如往列表头插入数据，就会导致大量单元行的刷新，所以应该避免这样简单随意地实现keyExtractor函数，而应该使用每个单元行数据能确定的唯一标识。当然如果可以肯定列表数据的顺序一定不会发生变化，那也没什么问题，只要明白keyExtractor是做什么用就行。

### 单元行组件的刷新

当FlatList刷新之后，FlatList内的所有单元行组件的virtualDom会和之前的进行比较，来判断各个单元行组件是否需要刷新。这要求我们明确每个单元行组件什么时候需要刷新，什么时候不需要。如果不是很理解的话，可以写一个很简单的demo，每次刷新给列表增加一些数据，demo部分代码如下

    renderItem = ({item}) => {
      return <Cell data={item} />
    }

    class Cell extends Component {  //换成PureComponent试试
      return <View style={{width:300,height:50}}>
        <Text>{this.props.data}</Text>
      </View>
    }
如果单元行组件继承自Component，那么每次刷新，所有的单元行组件都会重新render，但如果继承自PureComponent，就会发现只有新增的单元行才会render。这是因为Component即使props没变也会刷新，所以FlatList刷新时所有的单元行组件也都进行了刷新，而PureComponent会进行props的浅比较，所以data没变的单元行就没有刷新。实际项目中，简单的情况可以直接用PureComponent，复杂的时候就需要实现shouldComponentUpdate。我做的一个功能，在界面刷新时，只有屏幕上显示的第一个单元行需要发生变化，其余单元行不变，就是通过实现单元行组件的shouldComponentUpdate来进行控制的，否则所有单元行都刷一遍，就产生多余的重复刷新而影响性能了。

### getItemLayout

最后需要提一下getItemLayout，在源码中注释里有

> `getItemLayout` is the most efficient, and is easy to use if you have fixed height items.Adding `getItemLayout` can be a great performance boost for lists of several hundred items.

如果单元行的高度是可知的，那么实现getItemLayout接口对于性能优化有很大的好处，因为不用在渲染时临时计算每个单元行的尺寸了。
