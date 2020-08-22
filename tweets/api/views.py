import random

from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from ..models import Tweet
from ..forms import TweetForm
from ..serializers import TweetSerializer,TweetActionSerializer, TweetCreateSerializer

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    mySerializer = TweetCreateSerializer(data=request.data)
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
 
@api_view(['DELETE']) # OR POST
@permission_classes([IsAuthenticated]) 
def tweet_delete_view(request, *args, **kwargs):
    qs = Tweet.objects.filter(id=kwargs['tweet_id'])
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({'message' : "You cannot delete this tweet"}, status=404)
    obj = qs.first()
    obj.delete()
    return Response({'message' : "Tweet Deleted"}, status=200)

@api_view(['POST']) 
@permission_classes([IsAuthenticated]) 
def tweet_action_view(request, *args, **kwargs):
    '''
        options are like, tweet and retweeet
    '''
    mySerializer = TweetActionSerializer(data=request.data)
    if mySerializer.is_valid(raise_exception=True):
        data = mySerializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == 'like':
            obj.likes.add(request.user)
            mySerializer = TweetSerializer(obj)
            return Response(mySerializer.data, status=200)
        elif action == 'unlike':
            obj.likes.remove(request.user)
            mySerializer = TweetSerializer(obj)
            return Response(mySerializer.data, status=200)
        elif action == 'retweet':
            new_tweet = Tweet.objects.create(user=request.user, parent=obj, content=content)
            mySerializer = TweetSerializer(new_tweet)
            return Response(mySerializer.data, status=201) 
        return Response({'message' : "Tweet Liked"}, status=200)


def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_qs = paginator .paginate_queryset(qs, request)
    mySerializer = TweetSerializer(paginated_qs, many=True)
    return paginator.get_paginated_response(mySerializer.data) #Response(mySerializer.data, status=200)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tweet_feed_view(request, *args, **kwargs):
    user = request.user
    qs = Tweet.objects.feed(user)
    return get_paginated_queryset_response(qs,request)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username')
    if username != None:
         qs = qs.filter(user__username__iexact = username)
    # mySerializer = TweetSerializer(qs, many=True)
    # return Response(mySerializer.data, status=200)
    return get_paginated_queryset_response(qs,request)


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
