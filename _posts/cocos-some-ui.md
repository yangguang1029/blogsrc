---
title: cocos之部分ui控件的使用
date: 2017-01-18 16:11:42
tags: cocos
---
现在cocos有了各种编辑器，需要手写ui的时候不是很多了，但也因为如此，偶尔需要手写的时候，反倒会因为陌生写出各种问题出来，而且对这些ui的接口比较熟悉的话，也有利于日常使用，所以这里稍微总结下部分ui控件的接口和使用,方便以后再用的时候快速回想起来，细节最好还是看源代码。

### scale9Sprite
- jsbinding代码位于 bindings/auto/jsb\_cocos2dx\_ui\_auto.cpp内
- c++代码位于cocos2d-x/cocos/ui/UIScale9Sprite.cpp内
- scale9的实现原理是将纹理根据设定的区域，生成9个sprite，然后batch渲染

用的比较多的接口有:

```
createWithSpriteFrame(SpriteFrame* spriteFrame);
createWithSpriteFrame(SpriteFrame* spriteFrame, const Rect& capInsets);
create(const std::string& file);

//实际显示大小
setPreferredSize(const Size& preferedSize)
//设定缩放区域
setCapInsets(const Rect& capInsets)
```
### EditBox
- jsbinding代码位于 bindings/auto/jsb\_cocos2dx\_ui\_auto.cpp内
- c++代码位于cocos2d-x/cocos/ui/UIEditBox/UIEditBox.cpp内
- 只需要注意它的各个状态的sprite都是scale9即可

使用较多的接口有：

```
create(const Size& size, Scale9Sprite* normalSprite, Scale9Sprite* pressedSprite = nullptr, Scale9Sprite* disabledSprite = nullptr);

setFontSize(int fontSize);
setFontColor(const Color3B& color);
setPlaceHolder(const char* pText);	//提示字符串

getString();	//在C++接口是getText，注意名称不一样
```

### Controlbutton
- jsbinding代码位于 bindings/auto/jsb\_cocos2dx\_extension\_auto.cpp内
- c++代码位于cocos2d-x/extensions/GUI/CCControlExtension/CCControlButton.cpp内

使用较多的接口有

```
create(cocos2d::ui::Scale9Sprite* sprite)
create(const std::string& title, const std::string& fontName, float fontSize)

setPreferredSize(const Size& size)
setBackgroundSpriteForState(ui::Scale9Sprite* sprite, State state)
setEnabled(bool enabled)

//绑定事件
button.addTargetWithActionForControlEvents(this, this._onClickSend, cc.CONTROL_EVENT_TOUCH_UP_INSIDE);
```

### scrollView
- jsbinding代码位于 bindings/auto/jsb\_cocos2dx\_extension\_auto.cpp内
- c++代码位于cocos2d-x/extensions/GUI/CCScrollView/CCScrollView.cpp内
- 回调jsbinding位于bindings/manual/extension/jsb\_cocos2dx\_extension\_manual内
- scrollView本身的大小是viewSize。它内部有一个container，当我们执行addChild时，实际上是被加到了这个container里，它的大小比viewSize要大，所以才可以滚动，设置它的大小是setContentSize。这是与其他node的setContentSize方法不一样的地方，需要注意。

使用较多的接口有

```
create()
create(Size size, Node* container/* = nullptr*/)

setContainer(Node * pContainer)
addChild(Node * child, int zOrder, int tag)

setDelegate()
setDirection(Direction eDirection)

setContentSize(const Size & size)
setViewSize(Size size)
setContentOffset(Vec2 offset, bool animated/* = false*/)

//回调
scrollViewDidScroll(ScrollView* view)
```

### tableView
- jsbinding代码位于 bindings/auto/jsb\_cocos2dx\_extension\_auto.cpp内
- c++代码位于cocos2d-x/extensions/GUI/CCScrollView/CCTableView.cpp内
- 回调jsbinding位于bindings/manual/extension/jsb\_cocos2dx\_extension\_manual内,在这里也额外定义了一个create方法，而没有放在上面的jsbinding里
- js-bindings/bindings/script/extension/jsb\_ext\_create\_apis.js定义了新的构造函数cc.TableView.prototype._ctor = function(dataSouurce, size, container)，所以可以直接new
- 在jsbinding的init函数里，以及create函数里，都会自动调用一次reloadData，所以在js层代码中，新建一个tableView是不需要手动调用reloadData的，而C++代码则需要。 

使用较多的接口有

```
setDirection(Direction eDirection)
setVerticalFillOrder(VerticalFillOrder fillOrder)
reloadData()

//回调就不写了，基本上都会知道
```

### 其它
像checkbox,ControlSlider等用的不多的，可以临时去查一下。
