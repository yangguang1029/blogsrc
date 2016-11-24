---
title: svn忽略文件
date: 2016-11-17 11:28:59
tags: svn
---



在svn项目中，对于不需要加入版本管理的文件，可以使用svn propedit svn:ignore来进行设置

在执行这句之前，需要先设置好SVN_EDITOR环境变量，例如在~/.bash_profile内添加

```
export SVN_EDITOR=emacs
```

然后执行

```
svn propedit svn:ignore .
```
这里的.表示对当前目录进行设置，此时会打开你指定的编辑器界面，在里面写上你需要忽略的文件名或者正则表达式即可.
但这句命令，只会影响你指定的路径的子文件及文件夹，而不会递归影响到更深层次。例如在编辑界面填上

```
dir1
dir2/dir21/dir211
```
这里dir1会被忽略，而dir211不会，如果需要忽略dir211，要么在当前目录下执行svn propedit svn:ignore dir2/dir21 要么切换到dir2/dir21目录下执行svn propedit svn:ignore . 然后填写的内容都是dir211

在网上看到一个解释

```
Each and every directory in Subversion can be thought of its own
module, so there's no real way for Subversion to know that
foo/bar/barfoo is a directory in module /foo/bar, or a another
separate module module.

That means there's no way for Subversion to know how to handle
properties that can affect an entire directory tree. Plus, it would be
difficult to know exactly what parent directory is affecting a child
directory.
```

最后提醒一下，只有还没有被加入版本管理的文件会被忽略，如果文件已经加入了版本管理，那设置了忽略也没用。其次，设置了忽略的文件，仍然可以被添加进版本管理中。