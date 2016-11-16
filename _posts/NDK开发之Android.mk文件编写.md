---
title: NDK开发之Android.mk文件编写
date: 2016-08-15 20:32:06
tags: ndk
---
现在我们把android稍微写复杂些。在项目根目录下创建一个lib1文件夹

结构如图：

![img](../images/CB15E4FA-DF13-428F-A62B-B7C483DE4277.png)

test10.h和test11.h很简单，就是声明了两个方法

```
int test10();
int test11();
```

我们先看这个lib1文件夹内的Android.mk文件

```
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := test1
LOCAL_MODULE_FILENAME := libtest1

LOCAL_SRC_FILES := test1.cpp
LOCAL_C_INCLUDES := $(LOCAL_PATH)
LOCAL_EXPORT_C_INCLUDES := $(LOCAL_PATH)

include $(BUILD_STATIC_LIBRARY)
```

这里LOCAL_MODULE是外面引用这个库时候需要用到的名字，LOCAL_MODULE_FILENAME不写也可以，默认就是在LOCAL_MODULE前面加上lib

LOCAL_SRC_FILES和LOCAL_C_INCLUDES分别表示需要编译的源文件，以及头文件路径，像这里只使用了当前目录为头文件查找目录，所以test1.cpp里写法就是

```
#include <test10.h>
#include <test1/test11.h>

int test10(){
	return 1;
}

int test11(){
	return 2;
}
```

LOCAL_EXPORT_C_INCLUDES是对外提供的头文件搜索路径，他决定了外面在引用这个头文件时的搜索相对路径。它跟LOCAL_C_INCLUDES完全可以不一样。

知道LOCAL_C_INCLUDES和LOCAL_EXPORT_C_INCLUDES的作用，编译时出现No such file or directory错误就完全不用害怕了，哪个文件找不到，去看一下这两个路径是否对就可以了。

再来看看jni目录下Android.mk

```
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := learnNDK

LOCAL_SRC_FILES := learnNDK.cpp
LOCAL_C_INCLUDES := $(LOCAL_PATH)

LOCAL_STATIC_LIBRARIES := test1


include $(BUILD_SHARED_LIBRARY)

$(call import-module, lib1)
```

比原来就多了两行，LOCAL_STATIC_LIBRARIES := test1 表示引用名字为test1的库，这个名字就是上个文件里的LOCAL_MODULE，$(call import-module, lib1)这里指定了搜索引用库的Android.mk的路径，它是相对于NDK_MODULE_PATH，我们可以在ndk-build命令中指定这个参数，多个路径间使用:分隔

之后我们增加一个库lib2，它依赖于lib1，
它的cpp文件为

```
#include <test20.h>
#include <test11.h>

int test20(){
	return test11() + 2;
}
```

它的Android.mk如下

```
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := test2

LOCAL_SRC_FILES := test2.cpp
LOCAL_C_INCLUDES := $(LOCAL_PATH)
LOCAL_EXPORT_C_INCLUDES := $(LOCAL_PATH)

LOCAL_STATIC_LIBRARIES := test1

include $(BUILD_STATIC_LIBRARY)


$(call import-module, lib1)
```

加上对lib1的引用即可。

jni目录下的Android.mk加上

```
$(call import-module, lib2)
```

同时修改

```
LOCAL_STATIC_LIBRARIES := test2 test1
```

这里记住**依赖顺序为从左到右，被依赖的基础库必须往后放**

最后是执行的ndk-build命令，正确指定NDK_MODULE_PATH即可

```
ndk-build NDK_MODULE_PATH=/Users/imac-0003/Documents/workspace/learnNDK
```