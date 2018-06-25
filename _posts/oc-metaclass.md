---
title: ObjectiveC之初解MetaClass
date: 2018-06-14 20:18:36
tags: ObjectiveC
---
MetaClass的概念是每一个进阶iOS开发者都需要了解的概念，因为有的地方看得不是很容易理解，所以配合例子介绍一下概念。

在ObjectiveC中，每个类都对应着一个对象，我们把它叫做类对象，它其实是一个结构体struct objc_class。当这个类构造出一个实例后，实例的isa指针就指向了这个类对象。而类对象本身也有一个isa指针，它指向了这个类的元类MetaClass。元类也是一个struct objc_class，它也有一个isa指针，指向了NSObject的MetaClass，NSObject的MetaClass的isa指针指向了它自己。

如果上面那句话看懂了，就可以结束了。接下来是举证时间。

OC中，每个interface声明的类，最终基类都是NSObject，在NSObject中有一个静态方法class，它获取到的就是类对象的指针

    @interface TestISA1
    @end
  
    @interface TestISA2 : TestISA1
    @end
  
    Class c1 = [TestISA1 class];
    Class c2 = [TestISA2 class];
    NSLog(@"c1 : %p c2  %p ", c1, c2);  //c1 : 0x109e59e08 c2  0x109e59e58
然后查看它们实例的isa指针

    void printIsa (NSObject *c) {
      struct objc_object *f = (struct objc_object *)malloc(sizeof(struct objc_object));
      memcpy(f, c, sizeof(struct objc_object));
      NSLog(@"isa is %p", f->isa);
      delete f;
    }

    TestISA1 *t1 = [TestISA1 new];
    TestISA1 *t11 = [TestISA1 new];
    TestISA2 *t2 = [TestISA2 new];
    printIsa(t1);   // isa is 0x109e59e08
    printIsa(t11);   // isa is 0x109e59e08
    printIsa(t2);   // isa is 0x109e59e58
  可以看到，实例的isa指针就是类对象的指针。

  然后看看类对象的isa指针，也就是元类

    Class o = [NSObject class];
    //c1 : 0x109e59e08 c2  0x109e59e58 o 0x10ae6eea8
    NSLog(@"c1 : %p c2  %p o %p ", c1, c2, o);
    //c1 isa : 0x109e59de0 c2 isa  0x109e59e30 o isa 0x10ae6ee58
    NSLog(@"c1 isa : %p c2 isa  %p o isa %p", c1->isa, c2->isa, o->isa);
    //c1 isa isa : 0x10ae6ee58 c2 isa isa 0x10ae6ee58 o isa isa 0x10ae6ee58
    NSLog(@"c1 isa isa : %p c2 isa isa %p o isa isa %p", c1->isa->isa, c2->isa->isa, o->isa->isa);
  可以证明前面的说法，c1, c2对应的是各自类对象的地址，它们的isa指向了各自MetaClass的地址，再下一层meta就都是NSObject的MetaClass了。