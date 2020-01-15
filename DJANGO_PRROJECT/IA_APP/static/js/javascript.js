var messagesCount=0;
$(function() {
    $("#messageInput").keypress(function (e) {
        if(e.which == 13) {
            //submit form via ajax, this is not JS but server side scripting so not showing here
            messagesCount++;
            messageId="message_"+messagesCount;
            $("#messagesBox").append("<div class='userMessage' id='"+messageId+"'>"+$(this).val() + "</div>");
            let reply_text='';
            getBotReply($(this).val(),function(result){
            $("#messagesBox").append("<div class='botMessage'>"+result+"</div>");
            });
//            }

    		$('#messagesBox ').animate({
        	scrollTop: $('#'+messageId).position().top
    	}, 'slow');
    		  $(this).val("");
            e.preventDefault();
        }
    });
});

function getBotReply(str,callback) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var reply = JSON.parse(this.responseText);
      return callback(reply.reply);
    }
  };
  xhttp.open("GET", "bot_response/?text="+str, true);
  xhttp.send();
}

function getCategories(callback) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var categories = JSON.parse(this.responseText);
      return callback(categories);
    }
  };
  xhttp.open("GET", "get_category", true);
  xhttp.send();
}

function checkCategory(id){
  let category=document.querySelector('#'+id);
  setCategory(document.getElementById(id));
  if(category.dataset.checked=="true"){
    category.style.background="#888";
    category.style.border="3px solid transparent";
    category.style.opacity=".45";
    category.dataset.checked="false";
  }
  else{
    category.style.background="#41ac8e";
    category.style.border="3px dotted #16dcf1";
    category.style.opacity="1";
    category.dataset.checked="true";
  }
}

var active_categories;
getActiveCategories(function(result){
  active_categories=JSON.parse(result).active_categories;


var categories;
getCategories(function(result){
categories=result;
var index=0;
if(Object.keys(categories).length>0){
    for (key in categories) { 
      active='false';
      active_class='';
      for (ac in active_categories) {
        if(active_categories[ac]==categories[key]+'.aiml'){
          active='true';
          active_class='active_class';
          break;
        }
        }
        document.getElementById('categories').innerHTML+="<div data-checked='"+active+"' id='cat_"+index+"' class='"+active_class+" category' onclick='checkCategory(this.id)' data-file='"+categories[key]+".aiml'>"+categories[key]+"</div>";
        index++;
}
}
});
console.log(active_categories.active_categories);
});

function setCategory(element) {
  var file=element.dataset.file;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      window.alert(JSON.parse(this.responseText).result);
    }
  };
  xhttp.open("POST", "http://127.0.0.1:8000/toggle_category/", true);
  xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhttp.send("category="+file);
}


function getActiveCategories(callback) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var categories = JSON.parse(this.responseText);
    return callback(this.responseText);
    }
  };
  xhttp.open("GET", "get_active_categories", true);
  xhttp.send();
}



