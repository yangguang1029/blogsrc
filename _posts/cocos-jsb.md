---
title: cocos之jsbinding
date: 2017-01-06 10:31:04
tags: cocos
---

jsbinding是cocos通过引擎内置的spiderMonkey实现javaScript和C++交互的方案。当我们需要自己实现c++和js的互相调用时，基本上可以拷贝cocos引擎内的代码，cocos基于spiderMonkey的API进行了一些封装，使用起来比较方便。这篇博客只涉及我对代码的一些理解，如果想了解spiderMonkey的更多细节可以查看[官网](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey/JSAPI_User_Guide)。

如果能尽量看明白jsbinding的相关代码，在碰到问题时可以更快的解决，比如很常见的invalid native object报错，通过看代码可以知道它是找不到与js对象绑定的c++对象，比如js代码报错说某个方法是undefined时，我们可以去jsbinding的实现代码里查看一下这个方法是否封装进去了，比如一些类或者方法和属性在c++层和js层的名称不一样等等。


#### js调用C++代码

我们在AppDelegate.cpp里可以看到很多cocos的注册函数，通过这些函数，将c++类注册到js的环境中，然后就可以在js代码里构造这个类的实例，调用它的方法。我们基本上照抄就可以实现一个，代码就不贴了

- jsb\_myclass\_class->name 这个name就是在js代码中用来执行new时候的类名称
- JS\_SetProperty(cx, proto, "\_\_is\_ref", JS::FalseHandleValue); 根据C++类是否继承自Ref，设为True或者False
- 注册属性(静态属性和成员属性)和方法(静态方法和成员方法)，按照类似的格式去实现即可

```
	static JSPropertySpec properties[] = {
        JS_PSGS("myProp", _js_get_myProp, _js_set_myProp, JSPROP_PERMANENT | JSPROP_ENUMERATE),
        JS_PS_END
    };

    static JSFunctionSpec funcs[] = {
        JS_FN("func", js_MyClass_func, 0, JSPROP_PERMANENT | JSPROP_ENUMERATE),
        JS_FS_END
    };

```
- 我们在js代码中执行new MyClass时，就会调用C++层的 js\_MyClass\_constructor函数，在这里会新建一个c++对象，并新建一个js对象，然后建立映射关系，之后在互相调用的时候，才可以找得到彼此

```
bool js_MyClass_constructor(JSContext *cx, uint32_t argc, jsval *vp)
{
    JS::CallArgs args = JS::CallArgsFromVp(argc, vp);
    bool ok = true;
    MyClass* cobj = new (std::nothrow) MyClass();
    
    js_type_class_t *typeClass = js_get_type_from_native<MyClass>(cobj);  //从_js_global_type_map里获取，是在下面jsb_register_class的时候存进去的
    
    // link the native object with the javascript object
    
    JS::RootedObject proto(cx, typeClass->proto.ref());
    JS::RootedObject parent(cx, typeClass->parentProto.ref());
    JS::RootedObject jsObj(cx, JS_NewObject(cx, typeClass->jsclass, proto, parent));
    js_proxy_t* newproxy = jsb_new_proxy(cobj, jsObj);
    JS::AddNamedObjectRoot(cx, &newproxy->obj, "MyClass");
    
    
    args.rval().set(OBJECT_TO_JSVAL(jsObj));
    if (JS_HasProperty(cx, jsObj, "_ctor", &ok) && ok)
        ScriptingCore::getInstance()->executeFunctionWithOwner(OBJECT_TO_JSVAL(jsObj), "_ctor", args);
   //如果js层实现了_ctor方法，则调用它
    return true;
}
```
- 然后看一个简单的绑定C++函数到js中的实现。在这里我们看到了很眼熟的"invalid native object"。我们首先获取到js中的this，然后通过映射找到c++中的对象，然后调用方法即可。如果绑定静态方法，因为不需要实例，所以非常简单，直接执行即可。获取当前的js对象，并以此获取绑定的c++对象，这些代码能看懂并使用就足够了。

```
bool js_MyClass_func(JSContext *cx, uint32_t argc, jsval *vp) {
    JS::CallArgs args = JS::CallArgsFromVp(argc, vp);
    JS::RootedObject jsobj(cx, args.thisv().toObjectOrNull());
    js_proxy_t *proxy = jsb_get_js_proxy(jsobj);
    MyClass* cobj = (MyClass *)(proxy ? proxy->ptr : NULL);
    JSB_PRECONDITION2( cobj, cx, false, "Invalid Native Object");
    
    if (cobj) {
        cobj->func();
        return true;
    }else {
        JS_ReportError(cx, "Error: SocketIO instance is invalid.");
        return false;
    }
}
```

#### C++调用js

前面代码能差不多明白的话，c++调用js的其实也很好写，这里贴一段例子代码，它就不再是从cocos引擎内拷贝的，而是我自己写的

```
void MyClass::calljs() {
    JSContext *cx = ScriptingCore::getInstance()->getGlobalContext();
    
    js_proxy_t *proxy = jsb_get_native_proxy(this);
    JSObject* jso = proxy->_jsobj;
    
    std::string param = "test111";
    jsval jsparam = std_string_to_jsval(cx, param);
    JS::RootedValue retval(cx);
    std::string ret = "";
    std::string funcName = "calljs";
    
    bool success = ScriptingCore::getInstance()->executeFunctionWithOwner(OBJECT_TO_JSVAL(jso), funcName.c_str(), 1, &jsparam, &retval);
    if(success) {
        if(retval.isString()) {
           jsval_to_std_string(cx, retval, &ret);
            CCLOG("return....%s " , ret.c_str());
        }
    }else {
        CCLOG("excute failed ...");
    }
}
```
我们在C++代码中调用这个函数，它会调用绑定的对象在js中的calljs函数，并可以传递参数和接受返回值。

### tips
cocos封装了很多辅助函数，例如类型转换

```
jsval_to_std_string
std_string_to_jsval
OBJECT_TO_JSVAL
ccpoint_to_jsval
....
```
一般来说是够用了，需要的时候，多去引擎内部找找就可以了

另外，除了关注js-binding相关的代码外，cocos引擎在js层也有很多封装代码，位于js-bindings/bindings/script文件夹内。例如我们看tableView的jsbinding，它的构造方法是接受0个参数，但实际上我们可以这么写

```
var tableView = new cc.TableView(this, tsize);
```
原因就是在jsb_ext_create_apis.js内有这么一段

```
cc.TableView.prototype._ctor = function(dataSouurce, size, container) {
    container == undefined ? this._init(dataSouurce, size) : this._init(dataSouurce, size, container);
};
```
它在js层实现了_ctor方法，而我们前面说到，在jsbinding的constructor函数里，如果发现js对象有_ctor方法，则会调用它，所以这个方法被调用，它执行了_init方法。