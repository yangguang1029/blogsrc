---
title: c++之函数对象
date: 2017-03-10 19:32:37
tags: c++
---
std::function是一个类模板，定义于头文件\<functional\>。我们主要关注下它的几种生成方式。

- 直接指向函数。例如

```
bool func(int item) {
	return item % 2 == 0;
}

std::function<bool(int)> f = func;

```

- 使用lambda表达式。例如

```
int t = 3;
std::function<bool(int)> f1 = [t](int item) {
	return item % t == 0;
}
```

- 使用函数对象。例如

```
class Func(){
	private:
		int t;
	public:
		Func(int _t):t(_t){}
		bool operator()(int item) {
			return item % t == 0;
		}
}

std::function<bool(int)> f2 = Func(3);

```

- 使用std::bind绑定。例如

```
class Func1(){
	public:
		bool func(int item) {
			return item % 2 == 0;
		}
		bool func1(int _t, int item) {
			return item % _t == 0;
		}
}
func1 f1;
std::function<bool(int)> f3 = std::bind(&Func1::func, f1, std::placeholders::_1);
std::function<bool(int)> f4 = std::bind(&Func1::func, f1, 3, std::placeholders::_1);

bool func(in item) {
	return item % 2 == 0;
}
bool func1(int _t, int item) {
	return item % _t == 0;
}
std::function<bool(int)> fp5 = std::bind(func,  std::placeholders::_1);
std::function<bool(int)> fp6 = std::bind(func1, 3,  std::placeholders::_1);
```

使用函数对象的地方有很多，一个很典型的场景就是STL里的算法，经常会用到Predicate,它就是一个函数对象。例如

```
_InputIterator find_if(_InputIterator __first, _InputIterator __last, _Predicate __pred)
```
所以我们就可以直接拿上面的例子来使用，例如

```
vector<int> arr = {1,3,5,7,9,2,4,6,8};
auto iter5 = std::find_if(arr.begin(), arr.end(),fp5);
cout << *iter5 << endl;
```