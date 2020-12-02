function bicluster(opt){
 //to store the state of data
 this.left = opt.left || null;
 this.right = opt.right || null;
 this.vec = opt.vec;
 this.id = opt.id || 0;
 this.distance = opt.distance || 0.0;
}

function mergevecs(a,b){//merge two array 
 var mergdata = [];
for(var i=0;i<a.length;i++){
  mergdata.push((a[i] + b[i])/2.0);
 }
 return mergdata;
}

function hcluster(rows,distance){
 //row=>data,distance =>pearson
 var distances = {};
var currentclustid = -1;
var clust = [];
 for(var i=0;i<rows.length;i++){
clust.push(new bicluster({vec:rows[i],id:i}));//propagate an array with an object
 }
 
 //console.log(distance(clust[1].vec,clust[1].vec));
 var store=[];
 while(clust.length > 1){//loop until the lengt of the cluster array is greater than 1
let lowestpair= [0,1];//the lowest pair has index 0 and 1 if the array(i.e closest dist)
var closest =distance(clust[0].vec,clust[1].vec); 
   //console.lo(clust);
  for(var i=0;i<clust.length;i++){
   for(var j=i+1; j<clust.length; j++ ){
    var y = clust[i].id+","+clust[j].id; //store the id has string for object property
    
    if(!( y in distances)){//store the distance
     distances[clust[i].id+","+clust[j].id]= distance(clust[i].vec,clust[j].vec);
}
    var d = distances[clust[i].id+","+clust[j].id]
if(d < closest){//choose the lowest distance and store the index
     closest = d;
     lowestpair[0] =i;
     lowestpair[1] =j;
    }
   }
  }
var mergevec = mergevecs(clust[lowestpair[0]].vec,clust[lowestpair[1]].vec);
var newcluster = new bicluster({vec:mergevec,left:clust[lowestpair[0]],
          right:clust[lowestpair[1]],
          distance:closest,id:currentclustid});
  
  currentclustid -=1;//decrease the cluster id
  //store.push("("+lowestpair[1]+","+lowestpair[0]+")")
  
  clust.splice(lowestpair[1],1);
  clust.splice(lowestpair[0],1);
  clust.push(newcluster);
//lend--;
 }
  
 return clust[0];
}

function v(n){
 //function to space the output properly
 var space =[];
 for(var i =0;i< n;i++){
  space.push(' ');
 }
 return space;
}
function printclust(clust,labels,n){
 var space = v(n).join('')
 if(clust.id < 0){//indicate a group(parent)
  console.log(space+'-');
 }
 else{
  console.log(space+labels[clust.id]);// the child
 }
 
 
 if(clust['left'] !=null){
  printclust(clust['left'],labels,n+1);
  
 }
 if(clust['right'] !=null){
  printclust(clust['right'],labels,n+1);
  
 }
}


var euclid= function(v1,v2){
 var sum=0;
 for(var i=0;i<v1.length;i++){
  sum+= Math.pow(norm(v1)[i]-norm(v2)[i],2);
 }
 return sum;
};

var norm = function(numbers) {
    var max = Math.max(...numbers);
    var min = Math.min(...numbers);
    return numbers.map(v => (v-min)/(max-min));
}

var distFunc = function( a, b ) {
    return Math.abs( a - b );
};

var dtwDist = function( a, b ) {
    var dyn = new DynamicTimeWarping(norm(a), norm(b), distFunc);
	return dyn.getDistance();
};





function deepIterator (target, labels) {
  
  if (target['left'] != null)   {
    	deepIterator(target['left'], labels)
    	deepIterator(target['right'], labels)
    	target['name'] = ''
      //console.log(target['left']['name'])
      //console.log(target['right']['name'])
      
      target['vec'] = [target['vec']]
      target['vec'].push(target['left']['vec']) 
      target['vec'].push(target['right']['vec']) 

    	
      target['children'] = [target['left'], target['right']] 
    	delete target['left']
    	delete target['right']
    	delete target['id']
    	//delete target['vec']
    	delete target['distance']
  } 

  else {
  	target['name'] = labels[target['id']]
    delete target['left']
  	delete target['right']
  	delete target['id']
  	//delete target['vec']
  	delete target['distance']
  }
}


function flatten(array, mutable) {
    var toString = Object.prototype.toString;
    var arrayTypeStr = '[object Array]';
    
    var result = [];
    var nodes = (mutable && array) || array.slice();
    var node;

    if (!array.length) {
        return result;
    }

    node = nodes.pop();
    
    do {
        if (toString.call(node) === arrayTypeStr) {
            nodes.push.apply(nodes, node);
        } else {
            result.push(node);
        }
    } while (nodes.length && (node = nodes.pop()) !== undefined);

    result.reverse(); // we reverse result to restore the original order
    return result;
}





