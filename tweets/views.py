from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet

# Create your views here.

def home_view(request, *args, **kwargs):
    #return HttpResponse(f"<h1> Hello Afroze , {kwargs['tweet_id']} </h1>")
    return render(request, "pages/home.html", status = 200)


def tweet_detail_view(request, *args, **kwargs):
    """
        REST API VIEW
        consume by frontend 
        return json data
    """
    data = {
        "id" : kwargs['tweet_id']
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=kwargs['tweet_id'])
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    
    return JsonResponse(data, status=status)
