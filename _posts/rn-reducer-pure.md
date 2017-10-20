---
title: ReactNative中的reducer函数中的浅拷贝和深拷贝
date: 2017-10-16 20:15:36
tags: ReactNative
---

我们都知道reducer函数必须是纯函数，不能修改传入的state参数。先看一段示例代码

	export function updateData(state=[], action) {
    	switch(action.type){
        	case Actions.ADD:
            	return state.concat(action.data);
        	case Actions.UPDATE:
            	state[action.index] = action.data
				return state
        	default:
            	return state;
    	}
	}

这里state是一个简单的数组，ADD操作返回的是一个新的state，因为concat函数会创建并返回一个新的array。而UPDATE操作是修改了原state后返回原state。在demo中的表现就是，当reducer收到ADD时，会触发render刷新界面。而当收到update时，不会触发render，但如果再次收到ADD触发render刷新界面时，能看到UPDATE操作的数据已经被更新了。

结论就是

- 只要返回的是原state，就不会触发render。这也正是我们default需要返回state本身的原因。即使state数据发生了变化，也不会触发render，但数据的变化被存储起来了。
- 只要返回的是新state，就会触发render，即使数据完全不变

如果希望上面的UPDATE生效的话也很简单，把return state改成return state.slice(0)就可以了。但这种操作是不对的，虽然通过返回一个新的state来让render触发了，但它修改了state，它会导致的问题就是在component的componentWillReceiveProps函数里，nextProps和原来的props完全一致。reducer的原则是每个action对应着一个state，如果在action操作前后state相同，那就失去了这个特性了。

我们一般使用的Object.assign来构造一个新的state，Object.assign执行的就是浅拷贝而不是深拷贝，所以如果我们操作的state是一个比较复杂的结构，那么应该想办法手动执行深拷贝，否则使用浅拷贝的话，对应的内容就是同一份。

	export function updateDeep(state={sth:[]}, action) {
    	let sth = state.sth;
    	switch(action.type){
        	case Actions.ADD:
            	sth.push({data:action.data});
            	return Object.assign({}, {sth:sth})
        	case Actions.DELETE:
            	sth.splice(action.index, 1);
            	return Object.assign({}, {sth:sth})
        	case Actions.UPDATE:
            	sth[action.index].data = action.data;
            	return Object.assign({}, {sth:sth})
        	default:
            	return state;
    	}
	}

这个reducer函数直接修改了state.sth，虽然使用Object.assign返回了一个新的state，触发了render进行了刷新，但如果在componentWillReceiveProps函数里观察，就会发现this.props里的sth和nextprops里的sth是一模一样的，也就是执行action操作前后的state没有区分开来。

要解决上面的问题，可以有两种方案，一个是把reducer函数细分，确保在操作state时不会执行对对象进行浅拷贝。比如第二个例子的state改为[]，用combineReducer来合并细分后的reducer函数，但如果数组成员是Object，而不是简单数据类型，就仍然有浅拷贝的问题，所以可以用第二种方案，先把state深拷贝一份，然后修改这个拷贝后的state并返回，如果state是个很复杂的数据结构，深拷贝一次代价会比较大。所以实际中应该这两种方案结合起来。