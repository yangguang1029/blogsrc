---
title: addTouchToNode的实现
date: 2016-08-15 20:41:48
tags:
---
直接上代码

```
function addTouchToNode(node, touchEndCall, target, params) { //给node添加触摸事件
	var bTouchCanceled = false;
	var s = node.getContentSize();
	var rect = cc.rect(0, 0, s.width, s.height);
	var listener = node._tyTouchListener = cc.EventListener.create({
		event: cc.EventListener.TOUCH_ONE_BY_ONE,
		swallowTouches: true,
		onTouchBegan: function(touch, event) {
			var locationInNode = node.convertToNodeSpace(touch.getLocation());
			if (cc.rectContainsPoint(rect, locationInNode)) {
				bTouchCanceled = false;
				return true;
			}
			return false;
		},
		onTouchEnded: function(touch, event) {
			if (bTouchCanceled) {
				return;
			}
			var locationInNode = node.convertToNodeSpace(touch.getLocation());
			if (cc.rectContainsPoint(rect, locationInNode)) {
				if (touchEndCall) {
					touchEndCall.call(target, locationInNode, params);
				}
			}
		},
		onTouchCancelled: function() {
			bTouchCanceled = true;
		},

		onTouchMoved: function(touch, event) {
			var locationInNode = node.convertToNodeSpace(touch.getLocation());
			if (cc.rectContainsPoint(rect, locationInNode) == false) {
				bTouchCanceled = true;
			}
		}
	});
	cc.eventManager.addListener(listener, node);
	node.onEnter = function(){
		node.__proto__.onEnter.call(this);
		var listener = this._tyTouchListener;
		if(listener._isRegistered() === false) {
			cc.eventManager.addListener(listener, this);
		}
	};
};
```

这个方法经过了几次陆续的改进

1 .刚开始只实现了onTouchBegan和onTouchEnded，而且在onTouchEnded的时候，没有判断坐标是否在区域内，产生的bug是在区域内点击后，移动到区域外松手，也产生了点击。于是增加了onTouchEnded内的区域判断
2. 增加了onTouchCancelled和onTouchMoved接口，当触摸移动出区域时，取消掉触摸事件，如果模拟按钮，此时应该将图片缩小回初始大小
3. 重写onEnter方法，在onEnter内重新添加事件。为了解决当它自身或者父容器被移除后，重新添加时触摸事件失效的问题

经过这些完善后，基本上可以代替cc.MenuItemSprite来使用了，再稍微加上放大缩小的效果，就能当cc.ControlButton来使用。