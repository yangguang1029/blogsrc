---
title: ReactNative之props.children
date: 2018-02-28 20:18:36
tags: ReactNative
---
在github上看[react-native-on-layout](https://github.com/shichongrui/react-native-on-layout)的实现代码时，发现它把this.props.children当成一个函数使用，当时就奇怪了，我一直把this.props.children当做是一个object。然后去查了下[官方文档](https://reactjs.org/docs/jsx-in-depth.html)，找到了相关的介绍，于是大概翻译过来。

一般来说this.props.children会是以下几种类型

## 字符串

这是对于特定类型的component才有效，例如Text，写法也很简单

    <Text>i'm props.children</Text>
JSX语法中`In JSX expressions that contain both an opening tag and a closing tag, the content between those tags is passed as a special prop: props.children`，所以这个字符串其实就是props.children，只是我们一直没注意到而已。在这种情况下，字符串的首末空格会被忽略，空行会被忽略，换行符会被替换成空格。

## JSX Children

使用Component作为children，这是最常用的包含子节点的方法。例如

    <MyContainer>
        <MyFirstComponent />
        <MySecondComponent />
    </MyContainer>
当然对于可以使用字符串作为children的特殊组件，是可以混合使用的，例如

    <Text>123<Text>456</Text></Text>
原文中在这一段提到，一个component可以直接写成组件数组的形式，而不用封装在容器里，例如

    render(){
        return [<Text>1</Text>,<Text>2</Text>];
    }

这个真的是有些震惊了，如果我们return一个非component对象，实际上会直接报错。这里不同于我们平时写的使用{}包起来的数组，后面会说到，那是使用代码块作为children。这里我猜测是JSX做了特殊处理而已，如果返回数组，则把每个元素解析成一个组件，我们在实际开发中还是应该避免写成这样。

## 表达式

这也是我们经常使用的一种方式，用{}把表达式包围起来，例如

    <Text>123</Text>
    <Text>{"123"}</Text>
是一样的，所以如果想要Text显示带换行符的字符串，就可以这样

    <Text>{`123
    456`}</Text>
然后就是我们最常用的方式，实现组件数组，或者条件判断显示组件了，例如

    <View>
    {
        [1,2,3].map((item)=><Text>{item}</Text>)
    }
    {
        Math.random() > 0.5 ? <Text>123</Text> : <Text>456</Text>
    }
    </View>
它可以和其他几种类型混用，所以可以这么写

    <Text>
        123
        <Text>456</Text>
        {[<Text>789</Text>,<Text>10</Text>]}
    </Text>
当然实际开发中我们会尽量把代码结构写的工整一些。

## 函数

实际上props.children可以是任意类型，只是一般来说我们会以上面三种形式来使用它，但我们可以把它当做一个函数来使用，只要最后能形成一个合法的可渲染的组件，例如我们实现一个自定义组件

    class MyComponent{
        render(){
            let num = this.props.children(1);
            return <Text>{num}</Text>
        }
    }
    export default class Test extends Component{
        render(){
            return <MyComponent>
            {
                (num)=>num+1
            }
            </MyComponent>
        }
    }
这里我们在使用MyComponent时，包含在里面的是一个函数，所以在MyComponent的实现中通过this.props.children来调用这个函数，react-native-on-layout这个库就是这样实现的。

## Booleans, Null, Undefined

true,false,null,undefined都是合法的，只是不渲染任何东西。我们经常用这种方式来控制一个组件是否显示，用的比较多的是null。 需要注意有的值虽然会被当做false，但不是bool值，所以会被渲染，例如数字0。然后就是如果想要渲染这些值，应该转换成字符串。对下面的例子：

    <Text>{false}</Text>
    <Text>false</Text>
    <Text>{"false"}</Text>
第一种情况没有显示，后两者情况是一样的
