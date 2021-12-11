import sys

from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
import json
import spacy
from langdetect import detect

#using spaCy for similarity scoring

def compare(text1, text2, lang):
    lang_pckgs = {'en': 'en_core_web_lg', 'ru': 'ru_core_news_lg'}
    nlp = spacy.load(lang_pckgs[lang])
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)

#the view function for an end-point

@csrf_exempt
def requestView(request):
    if request.method=="POST":
        input = json.loads(request.body)
        if (not ("text1" in input.keys())) or (not ("text2" in input.keys())):
            response = JsonResponse({"Error:": "Your request must have \"text1\" and \"text2\" fields"})
            return response
        first, second = input["text1"], input["text2"]
        
        #detect texts language
        lang1, lang2 = detect(first), detect(second)
        
        accepted = ['ru', 'en']
        if (not (lang1 in accepted)) or (not (lang2 in accepted)):
            response = JsonResponse({"Error": "Please make sure that the text you provide is in accepted language. Only russian and english languages allowed."})
        elif lang1 != lang2:
            response = JsonResponse({"Similarity score:": 0})
        else:    
            response = JsonResponse({"Similarity score:": compare(first, second, lang1)})
        return response
    
    # for GET requests    
    elif request.method=="GET":
        return JsonResponse({'Usage:': 'Make a post-request with json structure, which must have fields "text1" and "text2" providing texts you want to compare. Currently only russian and english languages supported.'})

#urls

urlpatterns = [
    path("similar-recognition", requestView, name='similar-recognition')
    ]

#settings and manage

settings.configure(ROOT_URLCONF=__name__, ALLOWED_HOSTS=['*'])

if __name__=='__main__':
    execute_from_command_line(sys.argv)
