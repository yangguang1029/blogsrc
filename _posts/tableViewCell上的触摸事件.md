---
title: tableViewCell上的触摸事件
date: 2016-08-15 19:57:11
tags: cocos
---

### 1.tableCellTouched

这是最简单的处理tableViewCell上触摸事件的方法了，接口为

```
tableCellTouched:function (table, cell){}
```

它是基于对整个tableView的触摸，所以优先级会低于tableViewCell上的事件。

### 2.对tableViewCell添加事件

这个就是比较坑的了，我们知道tableView在滚动中，会把屏幕外的tableViewCell从container中移除

```
this.getContainer().removeChild(cell, true);
```

这里cleanup参数为true，也就意味着对这个cell绑定的所有事件都会被移除，所以如果直接对tableViewCell进行绑定事件，当这个cell被重用时，它的绑定事件已经无影无踪，不会再有响应了。如果只是触摸事件，那么直接用tableCellTouched接口即可，如果确实需要绑定特殊事件例如CustomEventListener，那需要将listener存起来，在tableCellAtIndex接口中每次都进行绑定，当然也可以重写tableCellView的onEnter方法，在里面添加。

### 3.tableCellView内子控件添加事件

例如往tableCellView内添加controlButton，这时候即使cell被重用，触摸事件仍然会响应，因为cleanup并不会递归对子节点调用，所以事件会被保留。(这里理解错误，cleanup会对所有子孙结点递归调用，移除其触摸事件。之所以controlbutton事件被保留了，是因为它在onEnter方法里重新添加了)不过在添加触摸事件时要小心，例如这段代码

```
tableCellAtIndex: function(table, index) {
    var cell = table.dequeueCell();
    if (!cell) {
          var cell = new cc.TableViewCell();
          var button =  new cc.ControlButton(new cc.LabelTTF("test", "Arial", 16), back)
          cell.addChild(button);
          button.addTargetWithActionForControlEvents(this, function(sender, event) {
            console.log(index);
          }, cc.CONTROL_EVENT_TOUCH_UP_INSIDE)
    } 
    return cell;
  }
```

这里点击按钮后显示的index肯定与期望的不一致，原因就是addTargetWithActionForControlEvents时传递的闭包内使用的index是tableViewCell构造时的index，当这个Cell被重用时，当前的index和构造时候的index很可能就不一致了。尤其是如果tableView方向是TABLEVIEW_FILL_TOPDOWN的话，tableView在构造时就发生了一次cell重用。如果希望显示正确的结果，必须使用cell当前的index来获取数据，也就是

```
button.addTargetWithActionForControlEvents(this, function(sender, e){
      var idx = cell.getIdx();
      console.log(idx);
  }, cc.CONTROL_EVENT_TOUCH_UP_INSIDE)
```

不使用controlButton，而是自己给子控件添加事件处理，也是一样的方法。