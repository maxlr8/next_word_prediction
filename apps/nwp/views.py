from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .utils import predict_next_word
# from apps.analytics.mixins import ObjectViewMixin
# from apps.analytics.signals import object_viewed_signal
import json, datetime
from .models import NWP
from .serializer import NWP_Serializer
from django.views.generic import DetailView
from django.contrib.auth.models import User

@login_required(login_url="/login/")
def lobby(request):
    if request.method == 'POST':
        saveselection(request)
    return render(request,'nwp/index.html')

@api_view(['POST'])
def nwp(request):
        if request.method == 'POST':
            if request.body:
                json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
            try:
                text = json_data.get('text')
                serializer = NWP_Serializer(data = text)
                if serializer.is_valid():
                    print(f'serializer okay --{text}')
                    # serializer.save()
                # model=json_data.get('model','BERT') 
                # topk = json_data.get('topk',3)
                predicted_words = predict_next_word(text)
                return Response({"message":"Sucess","time":datetime.datetime.now(),'data':predicted_words})


            except Exception as e:
                return Response({"message":"Failure","time":datetime.datetime.now(),'data':{"error":str(e)}})

def nwp_socket(text,user_name):
    user = User.objects.get(username=user_name)
    predicted_words = predict_next_word(text)
    sentence = NWP(user=user,sentence=text,predicted = json.dumps(predicted_words))
    sentence.save()

    return {"message":"Sucess","time":datetime.datetime.now(),'data':predicted_words,'user_resp':text,'objectId':sentence.object_id}

def saveselection(request):
    obj_id = request.POST.get('objectId')
    object_ = NWP.objects.get(object_id = obj_id)
    object_.selected = request.POST.get('selectedWord')
    object_.save()
    return {'success': True}


# class ProductDetailView(ObjectViewMixin, DetailView):
#     model = NWP
