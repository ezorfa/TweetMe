import random
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet
from .forms import TweetForm

# Create your views here.

def home_view(request, *args, **kwargs):
    #return HttpResponse(f"<h1> Hello Afroze , {kwargs['tweet_id']} </h1>")
    return render(request, "pages/home.html", status = 200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    if form.is_valid:
        obj = form.save(commit=False)

        obj.save()
        form = TweetForm()
    return render(request, 'components/form.html', context={"form" : form})


def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [{ "id" : x.id , "content" : x.content, "likes" : random.randint(0,100000)} for x in qs]
    data = {
        "isUser" : False,
        "response" : tweets_list
    }
    return JsonResponse(data) 


def tweet_detail_view(request, *args, **kwargs):
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
