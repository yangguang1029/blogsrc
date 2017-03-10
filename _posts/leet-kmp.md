---
title: leetcode之kmp算法
date: 2017-03-03 17:33:56
tags: leetcode
---

kmp算法用于查找子字符串，阮老师有一篇介绍的很细致的[博客](http://www.ruanyifeng.com/blog/2013/05/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm.html)基本上一遍就能看懂

整个流程可以概括为两步

1. 生成子字符串的部分匹配表，它是一个数组，对应子字符串上每个位置上的部分匹配值。 "部分匹配值"就是"前缀"和"后缀"的最长的共有元素的长度。"前缀"指除了最后一个字符以外，一个字符串的全部头部组合；"后缀"指除了第一个字符以外，一个字符串的全部尾部组合。
2. 匹配子字符串，如果子字符串匹配完，则查找成功，否则需要将匹配位置后移，后移的步数就是当前已匹配字符数量，减去最后一个匹配成功位置的部分匹配值

阮老师的文章里只讲了概念，没有算法，生成匹配表的算法，如果完全按照前后缀的概念去写，虽然能正确生成，但性能比较低。比如我写了一个

```
	//算出一个字符串的匹配值
    var getNext = function(str) {
    	var len = str.length;
    	if(len === 1) {
    		return 0;
    	}
    	var max = 0;
    	for(var i = 1; i < len; i++) {
    		if(str.slice(0, i) === str.slice(len-i)) {
    			max = i;
    		}
    	}
    	return max;
    }
    //算出needle的部分匹配表
    var nexts = [];
    for(var i = 0; i < nlen; i++) {
    	nexts[i] = getNext(needle.slice(0, i+1));
    }
```

实际使用的算法如下，又比较难理解。

```
	var nexts = [-1, 0];
    var j = 0;
    for(var i = 1; i < nlen; i++) {
    	while(j > 0 && needle[j] !== needle[i]) {
            j = nexts[j];
        }
        if(needle[j] === needle[i]) {
            j += 1;
        }
        nexts[i+1] = j;
    }
```
它的思路是这样的，因为我们是依次填充nexts，假设已经填充到ababa，此时nexts是[0, 0, 0, 1, 2, 3]，已经得到的最长共同前后缀分别是"", "", "a"="a", "ab"="ab", "aba"="aba"，此时i=5，我们需要求next[5]，如果needle[5] == needle[next[5]],也就是b，那我们就在前一个最长next值上加1就可以了，这个很好理解。但如果不是b，那我们就要在已有的对称'aba'='aba'里找它的最长公共前后缀，然后比较，在这个例子里我们可以看清楚的看到是'a'='a'，我们需要拿'a'后面的'b'与needle[i]比较，也就是needle[next[next[5]]]和needle[i]比较，这样直到找到0为止，这时表示没找到可用的对称，只好用needle[0]和needle[i]比较，如果相同，那么next[i]=1，否则为0。

这里nexts数组比needle多了1个长度，有的地方是这样，有的地方跟needle一样长，我觉得都可以，只是使用时候的区别。如果不是的话，欢迎指正。

