---
title: cocos之获取gzip压缩的http文本
date: 2016-12-06 20:23:38
tags: cocos
---

当使用http请求文本内容时，如果使用gzip压缩，可以大大减少字符串长度，提高传输效率。要实现此功能，客户端需要写一些代码：

首先是请求时候，设定好http头

```
std::vector<std::string> headers;
headers.push_back("Accept-Encoding: gzip,deflate")
request->setHeaders(headers);
```

然后在处理收到的消息时解压缩一下

```
std::vector<char> *buffer = response->getResponseData();
std::ostringstream outBuff;
for (unsigned int i = 0; i < buffer->size(); i++){
    outBuff << (*buffer)[i];
}
outBuff.flush();
std::string outstr = outBuff.str();
const unsigned char* tmp = (const unsigned char*)outstr.c_str();
size_t len = outstr.length();
unsigned char* outtmp = (unsigned char*)malloc(len);
ssize_t outlen = ZipUtils::inflateMemory((unsigned char*)tmp, len, &outtmp);
if(outlen > 0){
    outstr = std::string((const char*)outtmp);
    free(outtmp);
}else{
    CCLOG("inflate gzip content failed....");
}
```

ZipUtils是cocos基于zlib的封装，还有一些别的接口，需要的时候可以去看看