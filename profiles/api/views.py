import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from ..models import Profile

# Create your views here.
User = get_user_model()
ALLOWED_HOSTS = settings.ALLOWED_HOSTS


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def user_follow_view(request,username, *args, **kwargs):
    me = request.user
    other_user_qs   = User.objects.filter(username=username)
    if me.username == username:
        myFollowers = me.profile.followers.all()
        return Response({"count" : myFollowers.count()} , status=200)
    if other_user_qs.exists() == False:
        return Response({}, status=400)
    other = other_user_qs.first()
    profile = other.profile
    data= data = request.data or {}
    action = data.get("action")
    if action == "unfollow":
        profile.followers.remove(me)
    elif action == "follow":
        profile.followers.add(me)
    else:
        pass
    current_followers_qs = profile.followers.all()
    data = {
        "count " : current_followers_qs.count()
    }
    return Response(data , status=200)
