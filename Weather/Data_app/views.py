from django.shortcuts import render,redirect
from .models import City
import requests
from django.contrib import messages
from django.http import HttpResponseRedirect

# For Login 
def login(request):
    citiescount = City.objects.all().count()
    if citiescount < 25 :
        CityList=["Chennai","kerala","Coimbatore","Madurai","Tiruchirappalli","Salem","Tirunelveli","Vellore","Erode","Dindigul","Thanjavur","Karur","Hosur","Nagercoil","Kanchipuram","Namakkal","Sivaganga","Pollachi","Tiruppur","Cuddalore","Tiruvannamalai","Bengaluru","Mysuru","Bangalore","Mangalore"]
        c=abs(citiescount-26)
        cc=1
        url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=4b0171b2c9fa7eb0e434f805a8e78506&units=metric'
        while(cc!=c):
            for scity in CityList:
                city=scity.capitalize()
                check=City.objects.filter(name=city).exists()
                if check == False:
                    res=requests.get(url.format(city)).json()             
                    if res['cod']==200:
                        rcity = City()
                        rcity.name=city
                        rcity.save()
                        cc+=1
                        break
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return HttpResponseRedirect('allcities')
    return render(request,'login.html')


# To updata the data of the all cities.
def allcities(request):
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
    messages.success(request,"All Cities Data Updated...!!!")
    return render(request,'weather.html',context)


# For Search city data and display to user.
def search(request):
    cities=[]
    if request.method == 'POST':
        NCity=request.POST['name']
        url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=898029833a6727a791a149ddbb04a98d&units=metric'            
        res=requests.get(url.format(NCity)).json()                
        if res['cod']==200:
            cities.append(NCity)
            messages.success(request," "+NCity+" Displayed Successfully...!!!")
        else: 
            messages.error(request,"City Does Not Exists...!!!") 
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
    context={'data' : data}
    return render(request,'citysearch.html',context)


# For add city to the data base.
def addcity(request):
    if request.method == 'POST':
        scity=request.POST['name']
        city=scity.capitalize()
        CCity=City.objects.filter(name=city).exists()
        url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=898029833a6727a791a149ddbb04a98d&units=metric'
        if CCity==False:
            res=requests.get(url.format(city)).json()                
            if res['cod']==200:
                rcity=City()
                rcity.name=city
                rcity.save()
                messages.success(request," "+city+" Added Successfully...!!!")
            else: 
                messages.error(request,"City Does Not Exists...!!!")
        else:
            messages.error(request,"City Already Exists...!!!")
    data=City.objects.all()
    context={'data' : data}
    return render(request,'addcity.html',context)

# For delete the city form the data base.
def delete_city(request,CName):
    City.objects.get(name=CName).delete()
    messages.success(request," "+CName+" Removed Successfully...!!!")
    return redirect('addcity')
