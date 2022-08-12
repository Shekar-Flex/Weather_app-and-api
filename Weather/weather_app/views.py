from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from Data_app.form import CityForm
from Data_app.models import City
from django.contrib import messages
import requests


# For login
def home(request):
    if request.method == 'POST':
        name=request.POST['sname']
        pas=request.POST['pwd']

        user=authenticate(request,username=name,password=pas)
        if user is not None:
            login(request=request,user=user)
            url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=898029833a6727a791a149ddbb04a98d&units=metric'
            cities=City.objects.all()
            data=[]
            for city in cities:        
                res=requests.get(url.format(city)).json()  
                city_weather={
                    'city':city,
                    'temperature' : res['main']['temp'],
                    'description' : res['weather'][0]['description'],
                    'country' : res['sys']['country'],
                    'icon' : res['weather'][0]['icon'],
                }
                data.append(city_weather)  
            context={'data' : data,}
            messages.success(request,"Successfully Loged in...!!!")
            return render(request,'weather.html',context)
        else:
            return render(request,'login.html')
    return render(request,'login.html')


# For Logout
def logouts(request):
    logout(request=request)
    return redirect('home')