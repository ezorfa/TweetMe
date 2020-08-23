
from django.urls import path

from .views import profile_detail_api_view


urlpatterns = [
    path('<str:username>/', profile_detail_api_view),  #order matters because, django moves searches in order and stops at the first match
    path('<str:username>/follow', profile_detail_api_view),  #order matters because, django moves searches in order and stops at the first match
]
 