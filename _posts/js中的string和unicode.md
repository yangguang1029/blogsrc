---
title: js中的string和unicode
date: 2016-08-15 20:37:25
tags: javascript
---
javaScript中的String是UTF-16字符集合，但是要注意，因为js中并没有一种类型叫“字符”，所以charAt() 方法返回的是一个字符串。而charCodeAt()方法，则返回的是0-65535之间的一个整数。fromCharCode()方法是把一个unicode编码转换成String对象，这里是例如

```
'大'.charCodeAt(0)  ->  22823
"🐄".charCodeAt(1)  ->  56324
String.fromCharCode(22823) -> 大
String.fromCharCode(667736) -> じ
```

因为string是utf-16字符的合集，所以也可以直接用UTF-16编码来组成字符串，例如

```
var a = '\u0061\u5927' -> a大
```

如果这个utf-16字符是4个字节的，则它在length中反应的长度为2，例如

```
var a = "🐄";
console.log(a.length) ->2
a.charCodeAt(0) -> 55357
a.charCodeAt(1) -> 56324
```

这里顺便提一下utf-16的编码方式，如果是两个字节，则直接用两个字节表示，这其中0xD800到0xDFFF的字段，是被永久保留不被映射字符的，被用来做标记。超过两个字节，则把codePoint减去0x10000，得到一个长度为20bit的值，这个值的高10位被加上0xD800后，范围为0xD800到0xDBFF。后10位加上0xDC00后，范围为0xDC00到0xDFFF。