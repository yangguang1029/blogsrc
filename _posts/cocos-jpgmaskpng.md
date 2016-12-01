---
title: cocos之使用jpg+mask合成png实现方式（一）
date: 2016-11-28 16:11:09
tags: cocos
---

第一种方式，在CCImage内读取图片数据后，合并起来使用。改写Image类，增加initWithJpgAndPng方法

代码如下

```
bool Image::initWithJpgAndPng(const std::string& jpgpath, const std::string& pngpath) {
    bool ret = false;
    unsigned char* jd = nullptr;
    do{
        std::string jp = FileUtils::getInstance()->fullPathForFilename(jpgpath);
        Data jpgdata = FileUtils::getInstance()->getDataFromFile(jp);
        
        unsigned char* jdata = jpgdata.getBytes();
        ssize_t jsize = jpgdata.getSize();
        
        ret = initWithJpgData(jdata, jsize);
        if(!ret) {
            break;
        }
        
        int jwidth = _width;
        int jheight = _height;
        
        ssize_t jlen = _dataLen;
        jd = static_cast<unsigned char*>(malloc(jlen * sizeof(unsigned char)));
        memcpy(jd, _data, jlen * sizeof(unsigned char));	//将jpg数据暂存起来
        
        std::string pp = FileUtils::getInstance()->fullPathForFilename(pngpath);
        Data pngdata = FileUtils::getInstance()->getDataFromFile(pp);
        unsigned char* pdata = pngdata.getBytes();
        ssize_t psize = pngdata.getSize();
        ret = initWithPngData(pdata, psize);
        if(!ret) {
            break;
        }
        
        int pwidth = _width;
        int pheight = _height;
        if(pwidth != jwidth || pheight != jheight) {
            break;	//要求长宽必须严格相同
        }
        
        int pindex = 0;
        int jindex = 0;
        
        for(int index = 0; index < pwidth * pheight; index++) {
            unsigned char alpha =*(_data+(pindex+3));
            
            *(_data+pindex) = *(jd + jindex) * alpha / 255;
            *(_data+(pindex+1)) = *(jd + jindex+1) * alpha / 255;
            *(_data+(pindex+2)) = *(jd + jindex+2) * alpha / 255;
            
            pindex += 4;
            jindex += 3;
        }
    }while(0);
    
    if(jd) {
        CC_SAFE_FREE(jd);
    }
    
    return ret;
}

```
tips:

1. 这里为了验证思路，找了个RBGA8888的png做mask图，如果使用的mask图不是该格式，则需要修改\_renderFormat, \_fileType等属性。
2. 因为cocos默认png图片是pre\_multi\_alpha的，所以我们在加入alpha数据时，需要同时将alpha乘到rgb上

使用时代码如下:

```
Image* image = new Image();
    image->initWithJpgAndPng("res/test1.jpg", "res/test2.png");
    
    Texture2D* t = new Texture2D();
    t->initWithImage(image);
    Sprite* s = Sprite::createWithTexture(t);
    s->setPosition(480,320);
    this->addChild(s);
```