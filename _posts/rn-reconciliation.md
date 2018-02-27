---
title: ReactNative之VirtualDomTree的diff原理
date: 2018-02-25 19:15:36
tags: ReactNative
---
以前在解决一次flatlist没有局部刷新的问题时，写了一篇[博客](http://guangy.coding.me/2018/01/06/rn-flatlist-keyExtractor/)里面提到了官方的一篇文档叫做[reconciliation](https://reactjs.org/docs/reconciliation.html)。前阵子有人问我react的virtualDomTree的diff算法是怎么实现的，有没做什么优化点。我知道是这篇文章里的内容，但当时却说不清楚，这让我觉得我对这篇文章其实理解的并不够，所以把它再看一遍，然后把自己的理解记录下来，但这并不是翻译，完全是按照我自己的理解来写的，并不会非常严谨，但应该不会有误，如果有不同看法欢迎讨论。

正常来说，Dom树的diff算法复杂度是O(n^3)，如果页面很复杂时，性能就非常低了，比如有1000个节点的树，需要比较一亿次。React进行优化后，实际的复杂度降低到了O(n)，它基于两个原则：
1. 两个节点类型不同的话，以其为根节点的树也完全不同
2. 通过节点的key属性，可以定位新旧Dom树上对应的节点，来判定是否需要rerender

首先看如何比较，假定我们已经确定了要比较的节点
1. 如果节点类型不同，比如原来是Image，现在是View。那么以这个节点为根节点的整个Dom树都需要新建。它本身的属性，以及所有的子节点都没有比较的必要了。
2. 如果节点类型相同，那么就比较它的属性，只有那些发生了变化的属性会被记录下来，然后进行更新，没有发生变化的属性也就保持不变。然后循环遍历它的所有子孙节点进行比较。

需要注意一下，一旦一个节点比较有了diff，也就是变得dirty，那么它本身以及所有的子孙节点，都会变成dirty。diff会生成，但是否触发re-render取决于具体实现。不要误认为只要有diff必然会导致re-render，或者只要没触发re-render就没有diff。

然后就是我们怎么确定某个节点在新旧Dom树上如何对应的，假设下面这种场景

    //old
    <View>
        <Text>1</Text>
        <Text>2</Text>
    </view>
    //new1
    <View>
        <Text>1</Text>
        <Text>2</Text>
        <Text>3</Text>
    </view>
    //new2
    <View>
        <Text>3</Text>
        <Text>1</Text>
        <Text>2</Text>
    </view>
old指老的Dom树，new1在它的末尾插入了一个新的子节点，根据上面的原则，根节点View和Text1,Text2都没有变化，只是新增了Text3而已。但new2就不一样了，它在起始插入了一个Text3，这就导致Text1变成了Text3，Text2变成了Text1，然后新加了一个Text2，这显然是不太合适的，明明只增加了一个子节点，但三个都重绘了。例子中Text是一个很简单的组件，实际上它可以是一个非常复杂的根节点，那样的话可能就导致一整个Dom树的变动了。

解决这个问题的方案就是给Component添加了key属性。一个节点的所有子节点拥有一个唯一的key，注意这个唯一并不是全局的唯一，只需要跟它的兄弟节点区分开来就行。加上key之后再看上面的例子

    //old
    <View>
        <Text key="1">1</Text>
        <Text key="2">2</Text>
    </view>
    //new2
    <View>
        <Text key="3">3</Text>
        <Text key="1">1</Text>
        <Text key="2">2</Text>
    </view>
现在在进行diff时就知道了，key为1和2的Text节点内容没有变化，不会生成diff，只需要增加Text3就可以了。

文档里提到在项目开发中key的设置不要太过随意，例如直接使用index，如果这样，当子控件顺序发生变化时，可能就产生了额外的diff。我在使用flatlist时，keyExtractor直接使用index，导致在数组起始插入一个数据时，整个flatlist全部进行了刷新，而不是局部刷新，就是这个原因。

最后有两个结论：

1. 如果没有必要，不要轻易改变一个节点的类型。也就是说显示效果没变，却改变节点类型。这在实际情况中很少发生。
2. 使用一个稳定和唯一的key来让组件和它的兄弟组件区分，不使用或者不合理的使用可能造成性能问题。
