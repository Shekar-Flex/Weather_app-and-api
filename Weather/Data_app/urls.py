from unicodedata import name
from django.urls import path
from . import views 
from weather_app import views as view
urlpatterns = [
    path('',views.login,name='home'),
    path('login',view.home,name='login'),
    path('allcities',views.allcities,name="allcities"),
    path('search',views.search,name="search"),
    path('logouts',view.logouts,name="logouts"),
    path('addcity',views.addcity,name="addcity"),
    path('delete/<CName>',views.delete_city,name="DCity")
]