from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import aiml
import os
def index(req):
    return render(req,'IA_APP/index.html')
class ChatBot:
    def reply(self,text):
        kernel = aiml.Kernel()
        kernel.learn("IA_APP/aiml/test.xml")
        bot_response = kernel.respond(text)
        return bot_response

def bot_response(request):
    text=request.GET.get('text', '')
    bot=ChatBot()
    result=bot.reply(text)
    return JsonResponse({'reply':result})



