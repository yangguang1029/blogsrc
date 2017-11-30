---
title: ReactNative之ListView局部刷新
date: 2017-11-15 19:18:36
tags: ReactNative
---

我们直接来看一个很简单的demo，一个listView和一个button，点击按钮后，随机一行的数字加100。通过观察log可以看到，每次点击按钮后，_renderRow会被重新调用25次，每个MyComponent的render函数都被重新调用了一次。我们在dataSource的rowHasChanged回调里打了log，却发现没有被调用。所以虽然只改变了一行数据，却刷新了整个listView。这样肯定对性能会造成影响。这篇文章记录了修复这个bug的流程，如果不想看的话可以直接跳到最后看解决方案。demo代码如下

	class MyComponent extends Component{
    	render(){
        	console.log("guangy call render with tag " + this.props.tag);
        	return <Text>{this.props.text}</Text>
    	}
	}
	export default class TestList extends Component{
    	constructor(props){
        	super(props);
        	this.state = {
            	dataSource: new ListView.DataSource({
                	rowHasChanged: (rowData1, rowData2) => {
                    	console.log("guangy rowHasChanged")
                    	return rowData1 !== rowData2;
                		},
            	}),
            	data:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],
        	}
    	}

    	_renderRow(rowData, sid, rid){
        	console.log("guangy _renderRow");
        	return (<View style={{width:360,height:40,alignItems:"center",justifyContent:"center"}}>
            	<MyComponent tag={rid} text={rowData}/>
        		</View>);
    	}

	    render(){
        	return <View><ListView
            	style={{
                	width:360,
                	height:600
            	}}
            	dataSource={this.state.dataSource.cloneWithRows(this.state.data)}
            	renderRow={this._renderRow.bind(this)}
            	enableEmptySections={true}
        	/>
        	<Button title="click" onPress={()=>{
            	let arr = this.state.data;
            	let len = arr.length;
            	let index = Math.floor(Math.random() * len);
            	arr[index] += 100;
            	this.setState({data:arr});
        	}}/>
        	</View>
    	}
	}

既然是rowHasChanged不被调用，我们去源代码里找一下在哪里被用，然后就查到了ListViewDataSource的_calculateDirtyArrays方法，从方法名就能看出来，这是在计算哪些单元行变dirty了需要re-render。

	dirty =
          !prevSectionsHash[sectionID] ||
          !prevRowsHash[sectionID][rowID] ||
          this._rowHasChanged(
            this._getRowData(prevDataBlob, sectionID, rowID),
            this._getRowData(this._dataBlob, sectionID, rowID),
          );
所以一旦prevSectionsHash\[sectionID\]为false或者prevRowsHash\[sectionID\]\[rowID\]为false，_rowHasChanged回调就没机会被调用了。通过log也可以看到_calculateDirtyArrays函数传进来的实参prevSectionIDs和prevRowIDs是[]

调用这个函数的地方是ListViewDataSource的cloneWithRowsAndSections方法

	newSource._calculateDirtyArrays(
      this._dataBlob,
      this.sectionIdentities,
      this.rowIdentities,
    );
这里是创建了一个newSource,用来计算dirtyArrays的是原来的sectionIdentities和rowIdentities。看到这里就明白整个逻辑了，每次调用cloneWithRowsAndSections函数（调用cloneWithRows实质上也是一样），返回一个新的dataSource，然后计算需要re-render的单元行。

所以结论就是：要实现listView的局部刷新，关键是需要调用cloneWithRows或者cloneWithRowsAndSections来生成一个新的dataSource。将代码稍微改一下，测试就没问题了。

	//this.setState({data:arr});
	this.setState({dataSource:this.state.dataSource.cloneWithRows(arr)});
然后需要注意的是rowHasChanged回调函数，这个demo里使用的数据是简单数据类型，如果是复杂数据类型，简单的使用===就会有问题了，有可能实际数据内容没变化但引用变化了，导致不应该re-render但却触发了。或者实际数据内容变化了但是引用没变，导致应该re-render却没触发。简而言之就是复杂数据类型应该比较实际数据内容。


另外一个实现局部刷新的方案是将renderRow返回的Component进行封装，实现其shouldComponentUpdate接口。这个方法比较绕，所以最好还是使用ListView本身提供好的接口rowHasChanged。