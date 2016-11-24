---
title: cocos图片资源加密
date: 2016-11-24 18:30:23
tags: cocos
---

无意中看到[hnliu'sblog](http://blog.csdn.net/liuhannan111/article/details/52472012)上的方案，看完思路后，自己也照着写了一个，虽然不复杂，但是也花了将近两个小时。

python代码如下

```
import os
import random

ENCRYPTBYTE = random.randint(1,255)	#不能随机到0，否则等于没加密
FIRSTBYTE = 0x12
SECONDBYTE = 0X34
THIRDBYTE = 0x56

print("encrypt key is " + str(ENCRYPTBYTE))

def getNewFileName(path):
	arr = os.path.split(path)
	dirname = arr[0]
	filename = arr[1]
	nameArr = filename.split(".")
	return os.path.join(dirname, nameArr[0]+"-en." + nameArr[1])

def encrypt(path):
	rf = open(path, "r")
	newpath = getNewFileName(path)

	wf = open(newpath, "w")

	bytes = bytearray(rf.read())
	if bytes[0] == FIRSTBYTE and bytes[1] == SECONDBYTE and bytes[2] == THIRDBYTE:
		print "encrypted already, return"
	else:
		index = 4
		newarr = bytearray(len(bytes) + 4)
		newarr[0]= FIRSTBYTE
		newarr[1]= SECONDBYTE
		newarr[2]= THIRDBYTE
		newarr[3]= ENCRYPTBYTE
		for byte in bytes:
			newb = byte ^ ENCRYPTBYTE
			newarr[index] = newb				index += 1
		wf.write(newarr)
		wf.close()
	rf.close()
	
if __name__ == '__main__':
	encrypt("/Users/yangguang/project/test/test_cocosx/Resources/HelloWorld.png")
```

cocos端解析代码为把原来的initWithImageData改名为initWithImageDataInternal，然后重写initWithImageData方法

```
bool Image::initWithImageData(const unsigned char *data, ssize_t dataLen) {
    char first = *data;
    char second = *(data+1);
    char third = *(data+2);
    if(first == 0x12 && second == 0x34 && third == 0x56) {
        char key = *(data+3);
        unsigned char newarr[dataLen - 4];
        ssize_t pos = 4;
        while(pos < dataLen) {
            char old = *(data+pos);
            newarr[pos - 4] = old ^ key;
            pos += 1;
        }
        return initWithImageDataInternal((const unsigned char*)(&newarr) , dataLen - 4);
    }
    return initWithImageDataInternal(data, dataLen);
}
```

中间出了一个比较土的问题，就是python代码中newarr[index] = newb这句，用了newarr.append()，因为newarr初始化了大小，导致newarr前面全是0，数据都被添加到后面去了