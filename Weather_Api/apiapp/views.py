from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer,CityDataSerializer
from .models import User , CityData
import jwt, datetime
import requests


# For Creating new user.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




# For LOgin Authentication.
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        """
            Creating Token for Login session.
        """

        token=jwt.encode(payload=payload,key="secret",algorithm='HS256')

        response = Response()


        
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return Response({"Message " : " Login Successfull..."})




# To display user data.
class UserView(APIView):

    def get(self, request):

        """
        For Authentication purpose.
        """

        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(jwt=token,key="secret",algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        """
            To display the details of authenticated user.
        """
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)




# To Logout Authentication.
class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout success'
        }
        return response




# To View data in the api.
@api_view(['GET'])
def ViewData(request):


    """
        For Authentication purpose.
    """

    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(jwt=token,key="secret",algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')


    """
        create city for the first time is dose not exist.
    """

    citiescount = CityData.objects.all().count()
    if citiescount < 25 :
        CityList=["Chennai","kerala","Coimbatore","Madurai","Tiruchirappalli","Salem","Tirunelveli","Vellore","Erode","Dindigul","Thanjavur","Karur","Hosur","Nagercoil","Kanchipuram","Namakkal","Sivaganga","Pollachi","Tiruppur","Cuddalore","Tiruvannamalai","Bengaluru","Mysuru","Bangalore","Mangalore"]
        c=abs(citiescount-26)
        cc=1
        url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=4b0171b2c9fa7eb0e434f805a8e78506&units=metric'
        while(cc!=c):
            for scity in CityList:
                city=scity.capitalize()
                check=CityData.objects.filter(name=city).exists()
                if check == False:
                    res=requests.get(url.format(city)).json()            
                    if res['cod']==200:
                        rcity = CityData()
                        rcity.name=city
                        rcity.temperature= res['main']['temp']
                        rcity.description= res['weather'][0]['description']
                        rcity.country = res['sys']['country']
                        rcity.icon = res['weather'][0]['icon']
                        rcity.save()
                        cc+=1
                        break

    """
        Make the serializer and send api data.
    """
    citydata=CityData.objects.all()
    serializer = CityDataSerializer(citydata, many=True)
    return Response(serializer.data)




# To Update all Data of api.
@api_view(['GET'])
def UpdateData(request):

    """
        For Authentication purpose.
    """

    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(jwt=token,key="secret",algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    
    
    
    """
        Update all data of api and change to api.
    """

    citiesdata = CityData.objects.all()
    for city in citiesdata:
        url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=4b0171b2c9fa7eb0e434f805a8e78506&units=metric'
        res=requests.get(url.format(city.name)).json()             
        if res['cod']==200:
            newcity = CityData.objects.get(pk=city.id)
            newcity.temperature= res['main']['temp']
            newcity.description= res['weather'][0]['description']
            newcity.country = res['sys']['country']
            newcity.icon = res['weather'][0]['icon']
            newcity.save()
    return Response({"Message " : "All Cities Updated Successfully"})





# Seach city from the api.
@api_view(['POST'])
def SearchCity(request):


    """
        For Authentication purpose.
    """

    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(jwt=token,key="secret",algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    """
        Check City is Exist and get data from tha api and display to user.
    """
    cityname = request.data['name']
    cityname=cityname.capitalize()
    exist = CityData.objects.filter(name=cityname).exists()
    if exist == False:
        return Response({"Message ": "City Does Not Exist..."})
    citydata=CityData.objects.filter(name=cityname).first()
    serializer = CityDataSerializer(citydata, many=False)
    return Response(serializer.data)










# To Add City from api.
@api_view(['PUT'])
def AddCity(request):

    """
        For Authentication purpose.
    """

    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(jwt=token,key="secret",algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')


    """
        Check if the city is already in api.
    """
    cityname = request.data['name']
    cityname = cityname.capitalize()
    exist = CityData.objects.filter(name=cityname).exists()
    if exist == True:
        return Response({"Message ": "City Already Exist..."})

    """
        Check the city and add to the api.
    """
    
    url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=4b0171b2c9fa7eb0e434f805a8e78506&units=metric'
    res=requests.get(url.format(cityname)).json()             
    if res['cod']==200:
        newcity = CityData()
        newcity.name = cityname
        newcity.temperature= res['main']['temp']
        newcity.description= res['weather'][0]['description']
        newcity.country = res['sys']['country']
        newcity.icon = res['weather'][0]['icon']
        newcity.save()
        return Response({"Message ": "City Added Successfully..."})
    else:
        return Response({"Message ": "City Does Not Exist..."})







# To Delect The city from api.
@api_view(['POST'])
def DeleteCity(request):
    """
        For Authentication purpose.
    """
    token = request.COOKIES.get('jwt')
    print(token)
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(jwt=token,key="secret",algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    

    """
        For Get city name and delete from the api.
    """

    cityname = request.data['name']
    cityname = cityname.capitalize()
    exist = CityData.objects.filter(name=cityname).exists()
    if exist == True:
        citydel = CityData.objects.filter(name=cityname)
        citydel.delete()
        return Response({"Message ": "City Delete Successfully..."})
    else:
        return Response({"Message ":"City Does Not Exi..."})
