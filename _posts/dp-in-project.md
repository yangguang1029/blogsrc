---
title: 开发中使用到的设计模式
date: 2017-02-19 11:08:14
tags: 设计模式
---
### 单例模式 SINGLETON
单例在实际中使用很多，它保证一个类只有一个实例，并提供一个它的全局访问点。不论在cocos引擎还是自己的项目代码中，都有大量单例类的存在，但一般用于工厂类或者管理类，例如FileUtils, TextureCache等。保存一个全局变量并确保运行中只有一个实例，也可以看做是单例模式，比如在棋牌游戏中只会存在一个牌桌对象。

### 简单工厂模式 FACTORY
它在《设计模式》中叫做参数化工厂方法，它定义一个用于创建对象的接口，以一个参数作为标识符，来实例化对象。实际项目中有一个叫做WindowsManager::createWindow的方法，它根据传入的参数，创建出各种类型的弹出消息窗口。

### 外观模式 FACADE
这个模式也很好理解，它为复杂的子系统提供一个高层接口，以使子系统更加容易使用。举个很简单的例子，牌桌上收到某人出牌的消息，需要做很多事情，刷新他的剩余手牌数，展示他打出的牌，播放语音等等。我们把这些操作集合成一个接口，这样使用起来更方便，而且屏蔽了接口的内部实现，实现解耦合。但我们在写这个功能时，实际上并不一定需要创建一个facade类，而只是简单地封装一个函数就可以，只要理解这个概念就可以了。

### 观察者模式 OBSERVER
它定义了一种一对多的依赖关系，这个模式中的关键对象是目标(subject)和订阅者(observer)。这个模式不管是在cocos引擎内还是实际项目中都用到了。例如cocos引擎内，给一个Node添加触摸事件 就是订阅者向目标执行注册，当触摸事件发生时，目标会通知所有注册了的Node。它可以实现目标和订阅者的松耦合。

### 组合模式 COMPOSITE
将对象组合成树形结构，使得用户对单个对象和组合对象的使用具有一致性。 说到树形结构，第一反应就是cocos引擎的UI树了，它也确实是这个模式的应用，作为容器的类 Scene, Layer, Node，本身也是一个Node，使用起来就很方便。

### 适配器模式 ADAPTER
它将已有的接口转换成实际需要的接口。在《设计模式》中分为类适配器和对象适配器。在实际项目中，最明显的用到的地方，就是对不同平台sdk的封装，项目在接入各个平台时，他们的sdk功能都一样，无外乎登录，支付等等，但接口却不可能一样，我们通过构造一个adapter，把各种登录接口统一成一个，各种支付接口统一成一个，实际调用的时候就只需要调用这个统一的接口了。它的实现有两种方案：类适配器和对象适配器，前者使用继承，后者使用组合。

### 中介者模式 MEDIATOR
它用一个中介对象来封装一系列对象的交互，使得各对象不用显示的相互引用。在cocos引擎内，CCDirector就是一个中介者，通过它可以获取很多对象，比如getTextureCache, getActionManager等等，这些对象要交互的时候，彼此不需要持有引用，通过中介来获取就行了。实际项目中我将tableController作为一个中介者，牌桌上的各个子系统比如cardsController, operateController等等，都可以彼此不持有引用。

### 代理模式 PROXY
这个模式可以这样解释：我们想要一个实体subject，但出于某些原因，我们使用了一个代理proxy来代替它，为了能正常使用，显然我们构造的这个代理，必须与subject的接口保持一致。

在项目中有过一个例子，我们有一个通用的类soundManager，它有两个接口playMusic和playEffect。在不同的插件游戏中，播放声音和音效都是调用的这两个接口，但不同插件游戏中有不同的要求，A游戏要求播音乐时静音，B游戏要求播音效时静音，我们在不同插件中就构造不同的proxy类，它只为了代替soundManager而存在，同时也通过代替soundManager来实现了自定义的功能。当然proxy还适用于别的一些需要的场景。

### 享元模式 FLYWEIGHT
享元模式不要误认为是缓存池的概念，享元模式是在设计对象结构时，将可以共享的部分抽象出来进行建模。以达到减少存储开销的目的。被共享的flyweight不应直接实例化，而是通过FlyweightFactory来查找以保证共享。

### 装饰模式 DECORATOR
装饰模式用于动态的给对象添加额外的职责。因为装饰对象decorator要代替原组件component使用，所以接口要保持一致，在C++中通过公共父类的方式实现。装饰模式比使用继承更灵活，也避免在层次结构高层的类有太多特性。但decorator还是和component不是一样，decorator只是一个包装。

### 桥接模式 BRIDGE
桥接模式将抽象部分与它的实现部分分离，使它们可以独立变化。分离接口和实现部分有助于更好的结构化，比使用继承更为灵活。桥接模式适合用于分离不同维度的变化。
