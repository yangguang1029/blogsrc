---
title: iOS之dispatch_async和dispatch_sync
date: 2018-04-19 20:18:36
tags: iOS
---
最近开始搞iOS开发，但是对ObjectiveC还不太了解，所以记录一些iOS相关的知识。dispatch_async一般用于异步操作，但是dispatch_sync并不会新开线程，用在什么场景就不明白了，通过下面的例子可以稍微了解下。

    static int a = 0;
    static dispatch_queue_t asyncQueue() {
        static dispatch_queue_t bundleQueue;
        static dispatch_once_t onceToken;
        dispatch_once(&onceToken, ^{
            bundleQueue = dispatch_queue_create("asyncQueue", DISPATCH_QUEUE_CONCURRENT);
        });
        return bundleQueue;
    }
    -(void)func{
        for(int i = 0; i < 1000000; i++){
            a += 1;
        }
        NSLog(@"a is %d", a);
    }

    -(void)viewDidLoad{
        dispatch_async(asyncQueue(), ^{
            [self func];
        });
        dispatch_async(asyncQueue(), ^{
            [self func];
        });
    }

上面这个例子中，通过dispatch_async开启了一个新的线程，然后把两个block加入到一个concurrent队列中，输出的结果是

    a is 1011467
    a is 1049566
可以看到因为这两个block执行时都操作了变量a，互相产生了冲突。

如果我们把queue改成serial的，也就是

    bundleQueue = dispatch_queue_create("asyncQueue", DISPATCH_QUEUE_SERIAL);
可以看到结果变成了

    a is 1000000
    a is 2000000
这就是因为serial队列里的block不会重叠，一定会先完成一个，再去执行另一个。

可是有时候我们就需要queue是concurrent的，例如我们在block内做的是堵塞操作，那不可能一直留在这个线程里等着，这时将queue设成concurrent就会在被堵塞时新开一个线程去继续执行block，但又不希望冲突，就需要用dispatch_sync了，例如

    static dispatch_queue_t syncQueue() {
        static dispatch_queue_t bundleQueue;
        static dispatch_once_t onceToken;
        dispatch_once(&onceToken, ^{
            bundleQueue = dispatch_queue_create("syncQueue", DISPATCH_QUEUE_SERIAL);
        });
        return bundleQueue;
    }
    -(void)func{
        dispatch_sync(syncQueue(), ^{
            for(int i = 0; i < 1000000; i++){
                a += 1;
            }
            NSLog(@"a is %d", a);
        });
    }
此时结果也是

    a is 1000000
    a is 2000000
所以在asyncQueue是concurrent的情况下，在func函数里，通过dispatch_sync，给一个serial的queue里添加block，也保证了block的堵塞执行。如果把syncQueue改成DISPATCH_QUEUE_CONCURRENT， 则结果又变成了不确定。

上面总共有6种情况，asyncQueue为concurrent时，执行普通函数结果不确定，syncQueue为concurrent时结果不确定， syncQueue为serial时结果确定。 asyncQueue为serial时，执行普通函数结果确定，syncQueue不论为current还是serial结果都决定。如果抽象成结论的话，dispatch_sync和dispatch_async决定了是否新开线程，而concurrent和serial决定了block在执行时是否堵塞。

因为对iOS开发不是很熟，如有谬误欢迎指正。asyncQueue在concurrent时，如果线程被堵塞会继续新开线程的解释来自于[stackOverflow](https://stackoverflow.com/questions/6538744/dispatch-sync-vs-dispatch-async-on-main-queue)
    

