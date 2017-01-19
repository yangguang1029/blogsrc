---
title: 【leetcode】Minimum Moves to Equal Array Elements
date: 2016-12-05 14:41:30
tags: leetcode
---

[题目链接](https://leetcode.com/problems/minimum-moves-to-equal-array-elements/)

看完题目之后，稍微想了下，觉得不能用递归或者动态规划，于是老老实实的按题目意思写，每次进行排序，除了最大的数字外都加1，直到所有数字相等。提交之后，直接在测试用例[1, 2147483647]超时挂了，于是开始思考怎么解决，因为这是个easy难度的题目，所以思路倒是很快就有了。

将数组排序后，要让所有数字都相同，第一步很容易想到，就是把除了最大的数字每次加1，直到最大的数字有两个，它需要的步数就是最大数字和第二大数字的差。然后顺着这个思路，再通过累加，把最大的数字变成有三个，这需要的步数如果一时无法总结出公式，可以写个例子很容易看出来，是最大数字和第二大数字之差的两倍，以此类推即可。代码如下：

```
/**
 * @param {number[]} nums
 * @return {number}
 */
var minMoves = function(nums) {
    var mul= 1;
    nums.sort(function(left,right) {return left - right})
    var len = nums.length;
    if(len === 1) {
        return 0;
    }
    var re = 0;
    for(var i = len -1; i > 0; i--) {
        re += (nums[i] - nums[i - 1]) * mul;
        mul += 1;
    }
    return re;
};
```
