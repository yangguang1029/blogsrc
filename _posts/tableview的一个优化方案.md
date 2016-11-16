---
title: tableview的一个优化方案
date: 2016-08-15 20:03:29
tags:
---
### 方案说明

使用scrollView + bakeLayer(android) + batchNode(ios)来代替tableview。适用于tableCell数量不是很多且结构简单，但占用了大尺寸图片的情况。例如

![example](../images/720F3CD2-D65B-4F17-970F-797E8005AB6D.png)

这里中间的滑动界面，第一反应就使用了tableview来做。后来想在性能上做优化的时候，使用了scrollView + bakeLayer来代替。实现上很简单，只要将一个layer作为scrollview的container，并让其bake即可，构造时设定好每个cell的坐标。

官方关于bake的介绍点击[这里](http://www.cocos.com/doc/article/index?type=cocos2d-x&url=/doc/cocos-docs-master/manual/framework/html5/v3/bake-layer/zh.md)

### 为什么要用scrollview

为什么tableView不能直接使用bake呢？ 注意事项里**对于子节点经常会变的层， 启用bake功能，会给游戏性能带来额外的开销，建议对于不常修改子节点的层才开启该功能**

tableview的实现，会不停地将tableCell添加和移除，所以肯定不能直接取tableView的container出来直接bake

### 细节

这里的实现需要稍微注意的两点有：
1. container的尺寸要大于等于scrollView的尺寸，否则滑动时容易显示异常。如果container尺寸大于scrollView时，注意是否需要设置初始位移。
2. 添加触摸事件时，把触摸点坐标转换成container内的坐标，再根据各个cell在container内的位置即可判断点击了哪个cell 

### 代码

直接上代码

```
var cellheight = 206; //单元格高度
var cellcount = 6; //单元格数量
var row = Math.ceil(cellcount * 0.5);
var containerHeight = Math.max(cellheight * row, h);
var scrollHeight = h;    //scrollview高度
var scrollsize = cc.size(w, scrollHeight);

var container = new cc.Layer();
container.setContentSize(cc.size(w, containerHeight));

var scrollView = this._scrollview = cc.ScrollView.create(scrollsize, container);
scrollView.setDirection(cc.SCROLLVIEW_DIRECTION_VERTICAL);
scrollView.setPosition(cc.p(0, 119));
this.addChild(scrollView);

//因为方向是从上往下，如果container高度超出，则需要设置初始位移
var delta = scrollHeight - containerHeight;
if (delta < 0) {
    scrollView.setContentOffset(cc.p(0, delta), false)
}


for (var i = 0; i < cellcount; i++) {
    var s1 = new cc.Sprite("#hall_enter_" + i + ".png");
    var posx = i % 2 == 0 ? w * 0.25 : w * 0.75;
    var posy = containerHeight - (Math.floor(i / 2) + 0.5) * cellheight;
    s1.setPosition(posx, posy);
    container.addChild(s1);
}
container.bake();


var bTouchCanceled = false;
var touchBeganPos = cc.p(0, 0);
var that = this;
cc.eventManager.addListener({
    event: cc.EventListener.TOUCH_ONE_BY_ONE,
    swallowTouches: false,
    onTouchBegan: function(touch, event) {
        var bounding = scrollView.getBoundingBox();
        var pos = touch.getLocation();
        if (cc.rectContainsPoint(bounding, pos)) {
            bTouchCanceled = false;
            touchBeganPos = pos;
            return true;
        }
        return false;
    },
    onTouchEnded: function(touch, event) {
        if (bTouchCanceled) {
            return;
        }
        var loc = container.convertToNodeSpace(touch.getLocation());
        var col = loc.x < w * 0.5 ? 0 : 1;
        var row = Math.floor((containerHeight - loc.y) / cellheight);
        var index = 2 * row + col;
        that.onCellNodeClick(index);
    },
    onTouchCancelled: function() {
        bTouchCanceled = true;
    },

    onTouchMoved: function(touch, event) {
        var loc = touch.getLocation();
        if (Math.abs(loc.x - touchBeganPos.x) > 10 || Math.abs(loc.y - touchBeganPos.y) > 10) {
            bTouchCanceled = true;
        }
    }
}, container);
```

batchNode也是同理,我们抛弃tableCell，直接把组件添加到scrollView的container内，就可以使用batch功能了。