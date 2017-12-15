---
title: ES6中合并import
date: 2017-06-15 20:08:14
tags: javascript
---

最近打算优化一下ReactNative项目的代码，项目中有个公共模块文件夹utils，里面有不少文件，使用的也很频繁，这就导致了在很多js文件里都有这么一大段代码

	import * as A from "./utils/a" 
	import * as B from "./utils/b" 
	...
	import * as G from "./utils/g" 
	import * as H from "./utils/h" 
于是我就打算把整个utils内的文件做个汇总，具体实现方案是，在utils文件夹内添加一个index.js，其内容为

	import * as A from "./utils/a" 
	import * as B from "./utils/b" 
	...
	import * as G from "./utils/g" 
	import * as H from "./utils/h"
	export {A, B, ... G, H}
然后原来每个import utils内文件的地方，就改成了

	import {A, B, ... G, H} from "./utils/index"
我总结一下这样改的优劣。

好处是
1. 暴露一个唯一的接口，可以保持一致。原来在不同的文件里import同一个接口，可能取不同的名字，在这个文件里是`import * as A from './utils/a'`，另一个文件里就可能是`import * as B from './utils/a'`了，文件多了容易导致混乱，但我们统一成一个接口，除非特意使用as重命名，否则每个文件里都是一致的
2. 可以看出来用新的方法减少了一定的代码量，看起来舒服一些。RN本身也是这种风格，例如`import {Text, Button} from 'react-native'`。这样汇总尤其适合用于对外暴露接口。

当然也有一些不好的地方
1. 多维护了一个文件，当utils内新加文件时，需要到这个index.js内添加。
2. 被汇总的文件，要么只export default一个接口，要么以import *的方式被汇总。否则如果从这个文件里import若干个，再从另一个文件里import几个进来，然后汇总出去，就显得比较乱了，会分不清哪个接口是哪个文件的。

### 2017/12/15新加：

最近重构项目，把utils内一些文件挪到别的文件夹，这时才感受到汇总import再export最大的好处了，如果使用汇总的方案，那只需要改index.js一个文件，其余所有的都不用动。 但如果不进行汇总，那有多少个地方import了就需要改多少个地方，漏一个都报错。这应该是使用汇总方案最大的好处吧。
