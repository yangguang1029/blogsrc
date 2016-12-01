---
title: cocos之使用jpg+mask合成png实现方式（二）
date: 2016-11-28 17:47:08
tags: cocos
---

第二种方式就是使用shader，这种方式的优点是不需要修改源代码，但性能上不如第一种方式。

编写shader涉及到顶点着色器和片断着色器，前者使用sprite默认的即可。sprite使用哪个着色器，只要看一下CCSprite.cpp里这句就找到了

```
setGLProgramState(GLProgramState::getOrCreateWithGLProgramName(GLProgram::SHADER_NAME_POSITION_TEXTURE_COLOR_NO_MVP, texture));
```

然后我们稍微改动一下片断着色器，如下

```
#ifdef GL_ES
precision lowp float;
#endif
                                                          
varying vec4 v_fragmentColor;
varying vec2 v_texCoord;

uniform sampler2D mask;
                                                          
void main()
{
    gl_FragColor = v_fragmentColor * texture2D(CC_Texture0, v_texCoord);
    gl_FragColor.a = texture2D(mask, v_texCoord).a;
}
```

我们通过代码将mask作为一个Texture传进来，然后取它的每个像素的alpha值拿来用。

使用代码为:

```
    GLProgram *gp = GLProgram::createWithFilenames("res/test.vert", "res/test.frag");
    GLProgramState* gs = GLProgramState::create(gp);
    
    Image* img = new Image();
    img->initWithImageFile("res/zjz_pop_word_title_zhanji.png");
    Texture2D* t1 = new Texture2D();
    t1->initWithImage(img);
    
    gs->setUniformTexture("mask", t1);
    
    Sprite* s = Sprite::create("res/splash_tuyoo_m.jpg");
    s->setGLProgramState(gs);
    s->setPosition(480,320);
    this->addChild(s);
```

这里只需要小心一点不要把s->setGLProgramState(gs);写成s->setGLProgram(gp);就行，node上同时提供了这两个接口，但使用后者会创建一个新的GLProgramState，我们已经创建的gs也就失去了作用了