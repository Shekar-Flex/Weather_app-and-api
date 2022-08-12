from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView , ViewData , UpdateData , SearchCity ,AddCity,DeleteCity

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('viewdata',ViewData,name='viewdata'),
    path('updatedata',UpdateData,name="updtedata"),
    path('searchcity',SearchCity,name="searchcity"),
    path('addcity',AddCity,name="addcity"),
    path('deletecity',DeleteCity,name="deletecity")
]
