---
title: NDK开发之java调用C++
date: 2016-08-15 20:27:43
tags:
---
首先创建一个空的android项目，默认生成的MainActivity，修改如下

```
public class MainActivity extends Activity {

	static {
        System.loadLibrary("learnNDK");
    }
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		TextView t = (TextView)this.findViewById(R.id.textview);
		t.setText("" + hello(1));
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}
	
	public static native int hello(int num);

}
```

这里通过System.loadLibrary(“learnNDK”);来加载咱们等下要生成的动态库leanNDK

通过public static native int hello(int num);来声明一个C++层可以供我们调用的方法，返回值为int，函数名hello，接受一个形参int num

在项目根目录创建一个jni文件夹，执行命令

```
javah -d jni -classpath bin/classes/ com.example.learnndk.MainActivity
```

关于javah的详细参数介绍请参考[javah](http://docs.oracle.com/javase/7/docs/technotes/tools/windows/javah.html)

这里简单介绍一下，-d 表示输出的头文件目录，-classpath表示class文件的路径

然后就可以在jni目录下看到生成的文件com_example_learnndk_MainActivity.h

我们新建一个cpp文件来实现这个hello方法，新建一个learnNDK.cpp内容如下

```
#include <com_example_learnndk_MainActivity.h>

JNIEXPORT jint JNICALL Java_com_example_learnndk_MainActivity_hello
  (JNIEnv *, jclass, jint) {
  		return 99;
  }
```

然后在jni目录下，我们新建个Android.mk文件，内容如下

```
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := learnNDK
LOCAL_SRC_FILES := learnNDK.cpp

include $(BUILD_SHARED_LIBRARY)
```

然后使用ndk编译

```
ndk-build clean
ndk-build
```

成功之后，运行这个android程序，就可以看到结果了。

实际中Android.mk可以编写很复杂，也可能需要在jni目录下通过Application.mk来设定一些参数，如果不正确设定可能导致编译出错。