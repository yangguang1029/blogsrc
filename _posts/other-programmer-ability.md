---
title: 关于程序员工作能力的思考
date: 2017-12-07 15:50:39
tags: 其它
---

这个题目看起来就有点不着边，所以就当随便说说吧。昨天下午接到阿里游戏hr的电话问有没兴趣考虑亚博科技的cocos开发职位，我觉得可以了解下，于是对方说后期会有技术人员来电话沟通，挂了电话后，想想有大半年没有再接触cocos了，如果直接进行电话技术面，问起一些技术细节，我多半都不记得了，如果以此判定我技术不过关，我肯定是不承认的，但如果站在对方的角度想，你要求担任项目技术负责人的职位，却说不出个所以然来，对方又如何知道你的深浅呢。

程序员的面试一直是个很纠结的问题，网上相关的争论很多，追根到底就是如何判断一个程序员的工作能力。

先拿我自己的实际情况来说好了，我今年三月底到新的公司，工作是参与一个使用ReactNative进行app应用的开发，在此之前我从来没接触过RN，如果我直接冲着这个职位进来面试，那应该根本没有任何通过的希望，我本来面试的职位是cocos前端开发，阴错阳差给了我这个RN开发的职位。入职之后，首先因为我对NDK编译，C++,Java,JavaScript语言都比较熟，于是负责了一些原生语言和C++和JS之间API的设计实现。之后我独立负责完成了RN项目的Bundle拆分工作，这个工作需要对RN的源代码有一定的了解，我边看边学边实践，大概一个月的时间把现有的项目完成了bundle拆分。在入职后不久，看了下项目代码，因为原来的开发人员基本是原生开发人员转过来的，他们的JS代码和项目结构不是很规范，尤其是没有理解RN和web前端的数据流渲染方式的思想，所以提出了不少改进意见（大多数并没有落实下来，毕竟项目有点庞大，又有新的开发需求）。这是我这几个月做的事情，要说有多牛逼倒也不至于，但也不简单轻松，至少不谦虚的说我相信我是比身边的同事们都强一些，这也有工作业绩做证明，平时比较棘手的问题，需要跟踪深查出原因，或者可能修改源码，一般也交给我来解决。 

一个程序员的工作能力，在工作一段时间后，大家有目共睹了，也就不需要再证明了。然而在面试时，要怎么表现出来就是个问题了。今年年初我打算换工作时，也面试过几次，感觉其实都不太好。有一次是跟一个科大师兄一起吃饭，看能不能进入他们的U3D游戏开发项目组，同桌的还有他带来的几个技术leader，实际上也是一次面试，但我为了避免自己紧张，就当作一个普通的聊天，然后就没有然后了，我后来想想，也许是他们觉得我说的话都太空了吧，比如因为我这几年一直做cocos，没有U3D的开发经验，我就说新技术的学习其实是很简单的事，我现在也会这么说，因为我就是这么认为的。我从没接触过RN，但这几个月后，我敢说对RN的理解比很多人都强。如果说RN比较简单的话，那Unity,UE这些引擎又能多复杂吗？不过是工具而已，真正难的应该是计算机图形学吧，但实际项目中未必用到这么高深，技术能力深入到这么底层的专家也不多。

我觉得程序员的能力之一就是项目的代码结构设计，基本上每个程序员都知道MVC，即使是刚毕业的应届生，也能说得头头是道，但去看一个个实际项目就发现惨不忍睹了，UI和数据和逻辑代码全都混杂在一起，有人说这是很多现实原因造成的，比如项目进度比较赶啊，比如一份代码多人维护之类的，但我觉得其实是态度问题，一个认真的程序员，在动手写代码之前，要进行足够的思考，来找出最好的方案，不能只是为了把功能实现就行了。一般来说工作了三五年的程序员，如果还掌握不了一个项目的结构设计的话，那肯定是不够认真，没有经过思考。而这些不太好说清楚的东西，其实才是程序员最有价值的能力。

除此之外，我认为程序员最重要的能力就是解决问题的能力。碰到一个问题，通过观察思考定位到原因，然后从根本上解决，是一个好的程序员应有的能力。有的程序员在碰到问题的时候，不去想办法定位原因，很多时候靠猜测和尝试，看看这样改行不行，那样改行不行，这样的话即使问题可能解决了，但自己都不知道怎么解决的，以后碰到同样的或者类似的问题，解决起来还是很费力。还有的程序员在解决问题的时候很肤浅，比如一个component位置不对，不管是什么原因就直接改它坐标好了，结果改完在一些情况下还是不对，一个问题反反复复的折腾，可能最后还是没能彻底解决。这两种人其实都是在现实中很容易看到的。

上面两个是暂时能想到的，当然还会有别的方面，但说起来是一件事情，归根到底就是**认真**两个字。一个有技术追求的程序员，一定会想尽一切办法提高自己，努力思考，勤总结。要成为顶尖top 1%的明星程序员很难，但要成为在周围环境中突出的优秀程序员却不难，只要有认真的态度。我的这些看法在跟科大师兄聊的那次也说过，结果也显而易见，虽然我不知道他是否认同，但至少没能让他决定让我进入项目组，所以面试的时候我想也没必要说这些，还是多聊项目和技术细节好了，提前准备一下。

说了这么多，都是想到哪说到哪，就当是一次聊天来看吧。