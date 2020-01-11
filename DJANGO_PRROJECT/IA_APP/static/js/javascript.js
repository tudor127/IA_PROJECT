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