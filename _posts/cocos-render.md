---
title: cocos3.x 渲染机制简述
date: 2016-11-25 15:49:25
tags: cocos
---

cocos2dx-3.x对绘制部分进行了重构，将绘制从UI树的遍历中分离了出来。首先进行UI树的遍历给每个元素生成一个绘制命令。等遍历完之后，render开始执行栈中所有renderCommand。

### 遍历UI树

遍历UI树很简单，就是调用每个Node的visit函数，这是个虚函数，除了部分类做了重写(目前源代码里只有三个类重写了，分别是CCAttachNode, CCBillBoard, CCSprite3D)，其余就沿用了Node的实现。通过

```
void Node::visit(Renderer* renderer, const Mat4 &parentTransform, uint32_t parentFlags)
```
我们可以看到

1. 如果一个Node是不可见(_visible为false)，则不会生成渲染命令，因此隐藏的节点不会增加渲染负担，只会占用内存消耗。
2. 在遍历时，会对所有子节点以localZorder从小到大进行排序，如果localZorder相同，则以_orderOfArrival从小到大排序，这个子节点被添加的先后顺序。排序后先执行所有localZorder小于0的子节点的visit，再执行自己的draw，再执行所有localZorder大于0的子节点的visit。

draw函数为虚函数，且Node内的实现为空，具体实现在各个子类中，它的作用就是生成RenderCommand

### RenderCommand
RenderCommand有以下类型

```
enum class Type
    {
        /** Reserved type.*/
        UNKNOWN_COMMAND,
        /** Quad command, used for draw quad.*/
        QUAD_COMMAND,
        /**Custom command, used for calling callback for rendering.*/
        CUSTOM_COMMAND,
        /**Batch command, used for draw batches in texture atlas.*/
        BATCH_COMMAND,
        /**Group command, which can group command in a tree hierarchy.*/
        GROUP_COMMAND,
        /**Mesh command, used to draw 3D meshes.*/
        MESH_COMMAND,
        /**Primitive command, used to draw primitives such as lines, points and triangles.*/
        PRIMITIVE_COMMAND,
        /**Triangles command, used to draw triangles.*/
        TRIANGLES_COMMAND
    };
```
在CCRender.cpp的processRenderCommand函数里，有各个类型command的具体处理。例如 CUSTOM\_COMMAND就是执行设定的回调函数

通过这里可以了解cocos2dx-3.x的autoBatch机制，Sprite使用的是TrianglesCommand，在处理时，会先统一放在队列里，在遍历队列时，比较每个Command的materialID,如果相同则统一处理。决定materialID的有glProgram， \_textureID，\_blendType。此外不同globalZorder的精灵因为不在一批处理，所以不会自动autoBatch，不同父节点，不同localZOrder则不会影响，会自动autoBatch