import random

from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", status = 200)

@api_view(['POST'])
def tweet_create_view(request, *args, **kwargs):
    mySerializer = TweetSerializer(data=request.POST)
    if mySerializer.is_valid(raise_exception=True):
        mySerializer.save(user=request.user)
        return Response(mySerializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_detail_view(request, *args, **kwargs):
    qs = Tweet.objects.filter(id=kwargs['tweet_id'])
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    mySerializer = TweetSerializer(obj)
    return Response(mySerializer.data, status=200)
    
@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    mySerializer = TweetSerializer(qs, many=True)
    return Response(mySerializer.data)


# PURE DJANGOS ==============================================================
def tweet_create_view_pure_django(request, *args, **kwargs):
    '''
    REST API CREATE View -> DRF
    '''
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)

    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next_url") or None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        # console.log(request.is_ajax, "is ajax")
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url) 
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400);

    return render(request, 'components/form.html', context={"form" : form})


def tweet_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser" : False,
        "response" : tweets_list
    }
    return JsonResponse(data) 


def tweet_detail_view_pure_django(request, *args, **kwargs):
    """
        REST API VIEW
        consume by frontend 
        return json data
    """
    data = {
        "id" : Tweet.objects.get(id=kwargs['tweet_id']).id
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=kwargs['tweet_id'])
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    
    return JsonResponse(data, status=status)
