---
title: 使用closureCompiler深度混淆的一个坑
date: 2016-08-15 20:25:30
tags: google-closure-compiler
---
混淆命令为:

```
java -jar compiler.jar --compilation_level ADVANCED_OPTIMIZATIONS --js a.js --js_output_file b.js
```

混淆前代码

```
function test(result){
	console.log(result.fuck.text);
	console.log(result.text.fuck);
	console.log(result.color.colour);
	var tmp = {
		test1:Math.random(),
		"test2":Math.random()
	}
	for(var i = 0; i < result.length; i++) {
		console.log(result[i].text);
		console.log(result[i].text.text1.text2.text3);
		tmp.test1 += 1;
		tmp.test2 += 2;
		console.log(tmp.test1);
		console.log(tmp.test1.test11.test111);
		console.log(tmp.test2);
	}
	result.tmp = tmp;
}
```

混淆后代码

```
function d(b) {
	console.log(b.b.text);
	console.log(b.text.b);
	console.log(b.color.d);
	for (var a = {
			a: Math.random(),
			test2: Math.random()
		}, c = 0; c < b.length; c++) console.log(b[c].text), console.log(b[c].text.c.j.k), a.a += 1, a.b += 2, console.log(a.a), console.log(a.a.h.i), console.log(a.b);
	b.l = a
}
```

目前可以看到 text和color，在深度混淆中不会被混淆。是否还有别的一些关键字不被混淆，还不确定。比如colour就会被混淆= =