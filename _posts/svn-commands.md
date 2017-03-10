---
title: svn之使用命令行做分支管理
date: 2016-11-30 11:21:09
tags: svn
---
使用svn不论是做分支(branch)还是标签(tag)都是使用svn cp命令，他们本质上没有区别，但用途上可能不同，这完全取决于开发者，例如一般trunk是作为开发目录，branch是为了作并行开发，而tag是作为milestone管理。

新建一个分支使用命令svn cp，他会增加一次提交

```
svn cp trunk-url tag-url -m "testtag"
```

然后就可以把这个分支co下来

```
svn checkout tag-url
```

svn使用的是全局版本号，分支之间是共享版本号的。例如我们在trunk下做一次修改并提交后版本是1063，此时我们到tag目录下执行svn up，会显示版本号也到了1063，但并不会把更新拉取下来。要将trunk下的更新拉取过来，需要使用svn merge命令

进入tag目录执行

```
svn merge trunk-url
```
就把trunk上的改动合并过来了，也可以使用-r参数指定将某两次提交之间的diff合并过来

从trunk上提交，然后到tag下去merge也是一样。

删除分支，使用

```
svn rm tag-url -m "remove tag"
```

最后稍微解释下svn cp和svn merge两个命令
### svn cp
它的基本格式是：svn copy SRC DST,其中SRC和DST都可以是WC(working copy)或者URL

- WC->WC 这个只是对本地文件的拷贝后执行了svn add
- WC->URL 这个是拷贝后立即提交到了URL上，所以需要提供commit message
- URL->WC 这个将URL上拷贝到本地后执行了svn add，可以用这个命令带上-r版本号来找回被删除的文件
- URL->URL 这就是上面提到了创建分支了

### svn merge
作用是应用两组源文件的差别到工作副本路径，基本格式为

```
svn merge sourceURL1[@N] sourceURL2[@M] [WCPATH]

svn merge sourceWCPATH1@N sourceWCPATH2@M [WCPATH]

svn merge [[-c M]... | [-r N:M]...] [SOURCE[@REV] [WCPATH]]
```
例如

```
svn merge http://xxxx/a.json -r 1063:1064
svn merge ../config/ -r 1063:1064
```
如果不指定初始和结束版本号，则默认为仓库起始和当前（HEAD）


最近刚刚发现一个问题，初始仓库trunk，使用svn cp生成release仓库，然后在trunk上增加一行代码，svn merge到release上去，在release上删除，然后svn merge到trunk上去。此时这行代码处不会提示有冲突，而是默认添加上了这行。我不太确定是否我的用法不对，所以暂时先记录下这个情况。在分支间来回merge时，要小心合并，尽量避免频繁merge吧，毕竟每次merge会有很多冲突