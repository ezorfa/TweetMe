
from django.urls import path

from .views import user_follow_view


urlpatterns = [
    
    path('<str:username>/follow', user_follow_view),  #order matters because, django moves searches in order and stops at the first match
]
 