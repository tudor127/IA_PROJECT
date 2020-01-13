var templates;
function getCategories(callback) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var categories = JSON.parse(this.responseText);
      return callback(categories);
    }
  };
  xhttp.open("GET", "/get_category", true);
  xhttp.send();
}

function getCategory(file,callback) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var category = JSON.parse(this.responseText);
      return callback(category);
    }
  };
  xhttp.open("GET", "/get_aiml?file="+file, true);
  xhttp.send();
}

function showCategory(file,id){
        getCategory(file,function(res){
        cat=res;
        var j=0;
        if(Object.keys(cat).length>0){
        for (k in cat) {
        document.getElementById(id).innerHTML+='<b>'+k+'</b><p>'+cat[k]+'</p>';
        j++;

}
}
});
}

//getCategories(function(result){
//templates=result;
//var i=0;
//if(Object.keys(templates).length>0){
//    for (key in templates) {
//        document.getElementById('templatesBox').innerHTML+='<div class="templateBox"><div class="templateName">'+templates[key]+'</div></div>';
//        document.getElementById('categoryBox').innerHTML+='<div class="categoryBox" id="cat_id_'+i+'" onload="showCategory('+"'cat_id_1'"+')"></div>';
//        showCategory("cat_id_1");
//        i++;
//}
//}
//});
