---
title: cocos tips之jsbinding热加载
date: 2016-11-14 20:33:32
tags: cocos
---

所谓热加载，就是运行时，不用重启模拟器而重新加载js文件，提高开发效率。要实现热加载，首先要找到ocos是怎么加载js代码的，入口就是
ScriptingCore::runScript方法，包括在js代码内require，最终也是执行的这个方法。

在ScriptingCore::compileScript这个方法里，有

```
if (getScript(path)) {    
        return;
    }
```
这么一段代码，它读取了已加载文件的缓存，所以这几句必须注释掉，否则读取缓存的话，就没办法热加载了。

做了这步以后，在开启模拟器调试时，修改js代码后，不重启模拟器，只需要重新require一下文件，就实现了热加载了（比如做一个按钮，点击后重新require）。

然后如果你这么做，肯定会发现没有生效，原因是什么呢？那是因为我们在执行

```
require("a.js")
```
这句代码时，在模拟器上运行的时候，它实际加载的是

```
/Users/yangguang/Library/Developer/CoreSimulator/Devices/A25124E2-3204-43C7-A9F9-638FDF466587/data/Containers/Bundle/Application/69FC175C-06EB-4868-85D4-89F008164167/xxx.app/a.js
```
这样的路径，而我们修改的是项目中的代码，除非把修改后的代码拷贝到这个文件夹去，否则重新require的也是老代码，那要怎么解决这个问题呢？我们仍然看源代码，在读取js代码时，会获取这个文件的全路径，相关代码为

```
std::string FileUtils::fullPathForFilename(const std::string &filename)
{
    if (filename.empty())
    {
        return "";
    }
    
    if (isAbsolutePath(filename))
    {
        return filename;
    }
```
可以看到，如果文件路径写的是全路径，就不会再拼成模拟器应用所在路径了，所以解决的办法就出来了，我们将需要require的js文件的路径，在debug状态下设为开发目录下的全路径即可，在release状态下则为相对路径。

对于其他资源，也可以采用类似的思路，只要去掉资源缓存，以及使用全路径加载，就可以很容易实现资源热加载，从而避免调试时频繁的启动模拟器