---
title: git在错误分支上提交后的修正
date: 2016-08-15 20:22:43
tags:
---

应该在A分支上做的改动，不小心在B上改动并提交了，过了好几天才发现，此时需要做的操作包括，把这个提交移到A分支上，同时在B分支上把这个提交删除

移到A分支上很简单，在A分支上执行

```
git cherry-pick commitId
```

即可，有冲突的话，解决冲突

在B分支上的删除也简单，直接在B分支上执行

```
git reset commitId
```

这里的commitId是需要删除的提交之前的那个提交，然后把不想要的提交去掉，重新commit即可。这里写个简单的示例流程

```
touch a.txt
git add a.txt
git commit -m "add a"

touch b.txt
git add b.txt
git commit -m "add b"

git reset d9a3249  #这是add a之前的那个提交
git status  #此时可以看到a.txt和b.txt都是Untracked files，也就是从add a之后的所有提交都变成了没有add的状态

rm -rf a.txt
git add b.txt
git commit -m "reset"	#完成，add a这个提交已经没有了，而且在sourceTree上也看不到这次提交了
```

git reset d9a3249这步，也可以添加–soft参数，这个参数可以让所有的改动是已经add的状态，可以省掉之后再add一次，但要移除修改，则需要执行git rm –cached