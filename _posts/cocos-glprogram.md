---
title: cocos源代码之GLProgram
date: 2016-12-10 11:13:31
tags: cocos
---
### GLProgram和GLProgramState

在cocos内操作shader，基本就是使用GLProgram和GLProgramState这两个类，他们的关系，在官方注释里写着

```
GLProgramState holds the 'state' (uniforms and attributes) of the GLProgram.
 A GLProgram can be used by thousands of Nodes, but if different uniform values are going to be used, then each node will need its own GLProgramState
```
GLProgram是着色器的实现，GLProgramState是在Node上使用GLProgram的封装，所以我们在Node上应该操作GLProgramState，而不是GLProgram，例如设置uniform的值

### GLProgram的创建

第一步是init,主要是完成顶点着色器和片段着色器编译

第二步是link

- 调用bindPredefinedVertexAttribs，绑定一些默认的attribute，包括

```
const char* GLProgram::ATTRIBUTE_NAME_COLOR = "a_color";
const char* GLProgram::ATTRIBUTE_NAME_POSITION = "a_position";
const char* GLProgram::ATTRIBUTE_NAME_TEX_COORD = "a_texCoord";
const char* GLProgram::ATTRIBUTE_NAME_TEX_COORD1 = "a_texCoord1";
const char* GLProgram::ATTRIBUTE_NAME_TEX_COORD2 = "a_texCoord2";
const char* GLProgram::ATTRIBUTE_NAME_TEX_COORD3 = "a_texCoord3";
const char* GLProgram::ATTRIBUTE_NAME_NORMAL = "a_normal";
```
这样我们在顶点着色器内，就可以直接声明和使用这些变量名了，例如

```
attribute vec4 a_position;
attribute vec2 a_texCoord;
```
使用attribute修饰的变量，只能在顶点着色器中使用，且只能在顶点着色器中读取，不能赋值。

- 调用glLinkProgram进行链接，如果链接成功，调用parseVertexAttribs保存实际用到了的attributes，以及parseUniforms保存自定义的uniforms
- updateUniforms 将系统内置uniforms的使用情况存起来并更新


