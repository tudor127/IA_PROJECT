import base64
import hashlib

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect
import aiml
import json
import os
import xml.etree.ElementTree as ET
import Levenshtein
sessionId = 12345
def index(req):
    logged=req.COOKIES.get('logged', 'false')
    if logged=="true":
        return render(req,'IA_APP/index.html',{'logged':'true'})
    else:
        return render(req, 'IA_APP/index.html')

def login(req):
    logged=req.COOKIES.get('logged', 'false')
    if logged=="false":
        username = req.GET.get('username', '')
        password = req.GET.get('password', '')
        if username == "admin" and password == "admin":
            response = render(req, 'IA_APP/login.html',{'logged':'true'})
            response.set_cookie('logged', 'true')
        else:
            if req.GET.get('username', '') and req.GET.get('password', ''):
                response = render(req, 'IA_APP/login.html',{'not_logged':'true'})
            else:
                response = render(req, 'IA_APP/login.html')
            response.set_cookie('logged', 'false')
        return response
    else:
        return redirect("/administration")

def logout(req):
    response = render(req, 'IA_APP/login.html',{'logout':'true'})
    response.set_cookie('logged', 'false')
    return response


def similarities(inp):
    max_distance=int((30/100)*len(inp))
    data=[]
    min=100
    str=""

    for filename in os.listdir("IA_APP\\aiml"):
        filepath = os.path.join("IA_APP\\aiml", filename)
        if os.path.isfile(filepath):
            root = ET.parse(filepath)
            x = {}
            for category in root.findall('category'):
                pattern = category.find('pattern').text.strip()
                data.append(pattern)

    for index in data :
        if Levenshtein.distance(index.upper(),inp.upper())<min:
            min=Levenshtein.distance(index.upper(),inp.upper())
            str=index
    if min>max_distance:
        str="I don't understand!"
    return str

class ChatBot:
    def __init__(self, request):
        self.kernel = aiml.Kernel()
        self.learn(request)
        self.request = request

    # def learn(self, request):
    #     if not request.session.get('categories'):
    #         request.session['categories'] = ['test.xml']
    #     categories = request.session['categories']
    #     for i in categories:
    #         self.kernel.learn(os.path.join("IA_APP\\aiml", i))

    def learn(self, request):
        if request.session.get('sessionData'):
            data = request.session['sessionData']
            for key, value in data.items():
                if key[0] != '_':
                    self.kernel.setPredicate(key, value, sessionId)

        if not request.session.get('categories'):
            request.session['categories'] = ['test.xml']
        categories = request.session['categories']
        for i in categories:
            self.kernel.learn(os.path.join("IA_APP\\aiml", i))

    def reply(self, text):
        bot_response = self.kernel.respond(text, sessionId)
        self.request.session['sessionData'] = self.kernel.getSessionData(sessionId)
        if bot_response=="I don't understand!":
            if similarities(text)!="I don't understand!":
                bot_response=self.kernel.respond(similarities(text), sessionId)
            else:
                bot_response=similarities(text)
            return bot_response
        else:
            return bot_response

def bot_response(request):
    get_text = request.GET.get('text', '')
    text = bytes(get_text, "utf-8").decode("unicode_escape")
    bot = ChatBot(request)
    result = bot.reply(text)
    return JsonResponse({'reply': result})


def toggle_category(request):
    if request.method == 'POST':
        # print (request.session['categories'])
        category = request.POST.get('category', '')
        if os.path.isfile('IA_APP//aiml//' + category):
            if not request.session.get('categories'):
                request.session['categories'] = ['test.xml']
            l = request.session['categories']
            if category in request.session['categories']:
                l.remove(category)
                request.session['categories'] = l
                return JsonResponse({'result': 'Template '+category+' was removed from topics list'})
            else:
                l.append(category)
                request.session['categories'] = l
                return JsonResponse({'result': 'Template '+category+' was added to topics list'})
            # print (request.session['categories'])
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'File was not found'})
    # return JsonResponse({"res":category})

def get_active_categories(request):
    return JsonResponse({"active_categories":request.session.get('categories')})

def get_category(request):
    x = {}
    i = 0
    for root, dirs, files in os.walk("IA_APP\\aiml"):
        for name in files:
            if name.split(".")[-1] == 'aiml':
                x[name] = name.split(".")[0]
        return JsonResponse(x)

def get_aiml(request):
    filename = request.GET.get('file', '')
    filepath = os.path.join("IA_APP\\aiml", filename)
    if os.path.isfile(filepath):
        root = ET.parse(filepath)
        x = {}
        for category in root.findall('category'):
            pattern = category.find('pattern').text.strip()
            if not list(category.find('template')):
                template = category.find('template').text.strip()
            # x += pattern + " : " + template + "<br>"
            else:
                variante = []
                for el in category.find('template')[0]:
                    variante.append(el.text.strip())
                template = variante
            x[pattern] = template
        return JsonResponse(x)
    else:
        return JsonResponse({})

def get_aiml_content(file):
    filename = file
    filepath = os.path.join("IA_APP\\aiml", filename)
    if os.path.isfile(filepath):
        root = ET.parse(filepath)
        x = {}
        for category in root.findall('category'):
            if category.find('pattern').text:
                pattern = category.find('pattern').text.strip()
            if not list(category.find('template')):
                if category.find('template').text:
                    template = [category.find('template').text.strip()]
            else:
                variante = []
                for el in category.find('template')[0]:
                    if el.text:
                        variante.append(el.text.strip())
                template = variante
            x[pattern] = template
        return x
    else:
        return {}

def administration(request):
    logged=request.COOKIES.get('logged', 'false')
    categories={}
    category={}
    index=0;
    for root, dirs, files in os.walk("IA_APP\\aiml"):
        for name in files:
            if name.split(".")[-1] == 'aiml':
                categories[index] = name.split(".")[0]
                category[index] = get_aiml_content(name)
                index+=1
    if logged=="true":
        return render(request, 'IA_APP/administration.html',{'categories':categories,'category':category})
    else:
        return render(request, 'IA_APP/login.html')


def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem
def conv(data,output):
    #root element
    aiml = ET.Element('aiml', {'version':'1.0','encoding':'utf-8'})

    for key in data:
        category = ET.SubElement(aiml,'category')

        pattern = ET.SubElement(category, 'pattern')
        pattern.text=key

        template = ET.SubElement(category, 'template')

        random = ET.SubElement(template, 'random')
        if (type(data[key]) == list):
            for index in data[key]:
                li = ET.SubElement(random, 'li')
                li.text=index
        else:
            li = ET.SubElement(random, 'li')
            li.text = data[key]


    #write to file
    tree = ET.ElementTree(indent(aiml))
    tree.write(output)

# conv("input.json","output.aiml")

def edit_aiml(request):
    result="failed"
    if request.method == 'POST':
        filename = request.POST.get('file', '')
        if filename.strip()=='.aiml':
            return JsonResponse({"result":'Invalid Title'})
        js = request.POST.get('json', '')
        json_text=json.loads(js)
        conv(json_text,"IA_APP\\aiml\\"+filename)
        result="succes"
    return JsonResponse({"result":result})