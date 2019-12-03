---
title: ReactNative之一次Reconciliation讨论
date: 2019-10-09 21:15:36
tags: ReactNative
---
首先抛出一个问题，这也是这篇博客产生的背景，在[这个demo](https://github.com/yangguang1029/MyReactNative/blob/master/testReconciliation.js)里，有两个render函数，他们的效果是一样的，就是初始渲染Com1和Com2组件，5秒后变成只渲染Com2组件，但实现代码不一样，我看到一篇文章里说第二种写法性能更高，因为第一种写法会有组件的销毁和重新创建，第二种写法没有。读者不妨停下来自己想一想是否认同这个观点，然后再继续看下去。

我看到这个观点时，首先想到的是：这两种情况下最终渲染结果是一模一样的，所以我推断它们生成的virtual dom也是一样的，而组件（实际上是组件对应的原生view）的销毁创建，完全取决于virtual dom的布局，既然virtual dom一样，那这两种方案就没有区别，不存在后者性能更优的说法。于是我就去找作者讨论，作者使用ReactDevTools观察过这两种情况下的render数据，指出在第一种写法中，Com2组件重新构造了，render次数为1，而第二种情况下，Com2组件的render次数在增加，没有重新构造，这个可以在Com1和Com2的构造函数里打一句log，可以很容易验证。但我觉得这也很好解释，第一种情况下原来Com1位置变成了Com2，所以刷新时会卸载Com1和Com2然后装载Com2，这样来生成virtual dom，在这期间，类组件的实例化代价是非常非常小的，几乎不会造成任何性能差别。

本来以为讨论已经结束，结果作者观察后发现两种情况下virtual dom并不一致。两种情况下刷新前的渲染是完全一致的，但刷新后，第一种情况下根View下只有一个子节点Com2，而第二种情况下根View下有两个子节点，分别是null和Com2。于是我赶紧去翻了下React的[官方文档](https://reactjs.org/docs/react-component.html#render)

> Booleans or null. Render nothing. (Mostly exists to support return test && <Child /> pattern, where test is boolean.)

这里提到bool值和null不会渲染任何内容，但可没有说不会有virtual dom节点，而且实际观察确实有，于是前面得出的两种情况下virtual dom一样的这个结论就站不住脚了。（顺便说一下，这时我发现我前面因为实际渲染内容一样就推断virtual dom一样是很蠢的，因为搞错了因果关系，是virtual dom决定渲染内容，而不能由渲染内容来推断virtual dom）。不过虽然同意两种情况下virtual dom不一致，我仍然在做负隅顽抗，因为我脑子里揪住“两种情况的渲染结果一样”这个点不放，所以想是不是React在对virtual dom做diff时，忽略掉了这个null节点，这样即使virtual dom不一样，反应到原生端view时还是一样的，接着我就想，如果React能做到忽略掉null节点，那么在第一种情况下，它就不会笨笨的先卸载Com1和Com2然后装载Com2，而是通过virtual dom树的比较，发现Com2节点还在，所以复用Com2节点。

到这里，我觉得我的脑子已经不清醒了，第一种情况下Com2节点并没有被复用，是很明显的，React对virtual dom树的diff算法其实也并没有多深奥和复杂，官方在[Reconciliation](https://reactjs.org/docs/reconciliation.html)这一节介绍的也很清楚。所以很快我也就放弃了“React会很智能地帮我们安排好最高效的刷新方案”这个观点，应该靠事实说话，而不是盲目崇拜和迷信权威。

既然能实际观察到第一种情况下Com2销毁和创建了，第二种情况下没有，接下来我就开始思考是什么原因导致的，脑子不清醒的我又迅速掉入了一个坑，我想第一种情况下，return的两个js view不一样，是否导致它们在原生端绑定的不是同一个view呢？我不知道是否有人会觉得这句话很可笑，好在我自己迅速反应过来了：JSX只是语法糖，返回的js view并不代表任何意义！React的render原理是这样的：一个类组件要渲染时，调用它实例的render方法，得到virtual dom节点，进行diff，然后反映到原生view上。所以第一种情况下，return的是不是同一个js view根本没任何影响。

再次跳出坑之后，文章作者跟我说，第二种情况下Com2在父组件内的index没变，第一种情况下变化了，可能跟这个有关系。一句话点醒梦中人，我才突然明白过来，原来真相就是这么简单！React在对virtual dom做diff时，是按顺序一个一个来比较的，除非对组件给出key这个props，diff前后如果key相同，就会认为组件可以复用，这是Reconciliation中的一个重要内容。所以第一种情况下，刷新前后是Com1变成Com2，Com2销毁。而第二种情况下是Com1变成null从而销毁，Com2不变（当然位置变了，但组件不会销毁和创建）。

整个问题的讨论持续了有2个多小时，我原本以为自己对reconciliation非常了解了，但还出现“渲染结果一致所以virtual dom一致”这种低级错误，真的非常不应该，虽然得出结论后发现问题其实很简单，但整个思考过程还是挺有意思的，于是记录下来。

最后，在做demo验证时我发现一个很奇怪的问题，如下所示

````
  render() {
    return this.state.visible ? (
      <View style={styles.container}>
        {false}
        <Com1 />
      </View>
    ) : (
      <View style={styles.container}>
      <Com1 />
      </View>
    );
  }
````
刷新组件从false Com1变成Com1，理论上来说应该有一次Com1的销毁和创建，但实际上并没有，当增加子组件的个数，例如从false Com1  Com2变成Com1 Com2时，就和预期的一样了，所以为什么只有一个Com1时，没有发生组件的销毁和创建呢？这个我暂时没有答案，希望有大牛帮忙解答。