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


var categories;
getCategories(function(result){
categories=result;
var index=0;
if(Object.keys(categories).length>0){
    for (key in categories) {
        document.getElementById('categories').innerHTML+="<div data-checked='false' id='cat_"+index+"' class='category' onclick='checkCategory(this.id)'>"+categories[key]+"</div>";
        index++;
}
}
});

function setCategory(file) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML = this.responseText;
    }
  };
  xhttp.open("POST", "demo_post2.asp", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("fname=Henry&lname=Ford");
}