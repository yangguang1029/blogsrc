---
title: cocos之使用AssetsManager实现热更新
date: 2017-02-13 21:12:32
tags: cocos
---
cocos提供了AssetsManager类进行热更新。这里大概介绍下它的使用方法和内部原理，引擎使用的是v3.13。首先是一段简单的代码

```
    string url = "https://.....test.zip";
    string vurl = "https://.../version";
    string root = CCFileUtils::getInstance()->getWritablePath();
    string path =root + "test/";
    
    FileUtils::getInstance()->createDirectory(path);
    
    AssetsManager* am = AssetsManager::create(url.c_str(), vurl.c_str(), path.c_str(), [](int a){
        CCLOG("update failed %d", a);
    }, [](int b){
        CCLOG("update progress %d", b);
    }, [](){
        CCLOG("update success");
    });
    
    am->retain();	
    am->checkUpdate();
```
这里有两个地方特别需要需要注意：

- AssetsManager继承自Node，所以它的实例需要retain，否则无法正常工作
- 更新包的存储路径，必须是已存在的路径，否则会导致拷贝失败而报错

可以看到使用还是很简单的，构造的参数包括更新包url地址，返回最新版本号的url地址，更新包存储路径，下载成功回调，下载失败回调，下载进度回调。 然后调用checkUpdate就开始了整个更新流程，我们按照流程看一下源代码。

AssetsManager内部通过一个\_downloader来实现下载的

```
cocos2d::network::Downloader* _downloader = new Downloader();
```
它在构造函数里初始化，并设定好onTaskError, onTaskProgress, onDataTaskSuccess, onFileTaskSuccess四个回调。 

1. 当我们调用checkUpdate开始一次热更任务时，它使用\_downloader创建一个下载任务，根据\_versionFileUrl来获取需要更新资源的版本号。如果获取成功，会进入onDataTaskSuccess回调中，这里会获取本地存储的版本号，与之进行比较，如果相等，说明本地已经是最新版本，不需要更新。然后检查一下本地已下载版本，如果等于获取的版本号，说明更新包已经下载但尚未解压，直接执行解压操作。否则创建一个下载任务开始下载。
2. 在下载进度回调中，获取到当前下载的百分比
3. zip下载完成后，进行解压缩，如果失败，则把已下载成功的版本号记录在本地，避免再次下载。如果成功，则解压缩在我们设定的存储目录下，将本地版本目录更新至当前版本。删除已下载的zip文件，将存储目录添加到searchPath的最前面。

关于searchPath，它是一个队列，实现位于CCFileUtils内。cocos引擎在使用某个资源时，如果指定的资源路径不是绝对路径，就会依次使用searchPath内的路径合成一个绝对路径，如果找到了文件，就直接使用这个文件，所以我们热更新后的目录，设为searchPath的第一个，就可以实现替换掉老资源的功能。当然如果想节省空间，在下载成功的回调里，删除掉上个版本的目录就可以了。
