import random

from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.utils.http import is_safe_url

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    # username = None
    # if request.user.is_authenticated:
    #     username = request.user.username
    return render(request, "pages/feed.html")
  
def tweet_list_view(request, *args, **kwargs):
    return render(request, "tweets/list.html")

def tweet_detail_view(request, tweet_id ,*args, **kwargs):
    return render(request, "tweets/detail.html", context={'tweet_id' : tweet_id}, status=200)

def tweet_profile_view(request, username, *args, **kwargs):
    return render(request, "tweets/profile.html", context={'profile_usernmae' : username}, status=200)
