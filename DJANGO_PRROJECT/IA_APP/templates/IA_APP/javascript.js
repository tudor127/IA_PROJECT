var messagesCount=0;
$(function() {
    $("#messageInput").keypress(function (e) {
        if(e.which == 13) {
            //submit form via ajax, this is not JS but server side scripting so not showing here
            messagesCount++;
            messageId="message_"+messagesCount;
            $("#messagesBox").append("<div class='userMessage' id='"+messageId+"'>"+$(this).val() + "</div>");
            $("#messagesBox").append("<div class='botMessage'>Hello John</div>");
    		$('#messagesBox ').animate({
        	scrollTop: $('#'+messageId).position().top
    	}, 'slow');
    		  $(this).val("");
            e.preventDefault();
        }
    });
});