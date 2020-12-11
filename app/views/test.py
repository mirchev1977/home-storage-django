import json

from django.http import HttpResponse
from django.shortcuts import render

#from app.forms.profiles import ProfileForm
#from app.models import Profile, Expense
#from app.views.profiles import create_profile
from pip._vendor import requests

from app.models import User
from app.serializers import UserSerializer


def test(request):
    #get all Users
    #users = User.objects.all();
    #serializer = UserSerializer(users)
    #for user in users:
    #    user.delete()

    #serializer = UserSerializer(users)
    #if serializer.is_valid():
    #    serializer.save()

    #Update User
    #user = User.objects.last()
    #user = User.objects.get(pk=2)
    #user = User.objects.get(pk=3)

    #users = User.objects.filter(name="Gospodin Gospodinov")
    #for usr in users:
    #    serializer = UserSerializer(usr, data = {
    #        'id':    usr.id,
    #        'name': 'Kiro Kirov',
    #        'email': usr.email,
    #        'phone': usr.phone,
    #    })
    #    if serializer.is_valid():
    #        serializer.save()


        #seralizer = UserSerializer(data=user)
        #if seralizer.is_valid():
        #    seralizer.save()
        #user.save()

    #users = User.objects.all()
    #for usr in users:
    #    print(usr)

    #create an User
    #name = request.GET['name']
    #email = request.GET['email']
    #phone = request.GET['phone']
    #user = UserSerializer(data={'name': name, 'email': email, 'phone': phone })
    #if user.is_valid():
    #    user.save()

    #r = requests.get('https://mirchev-home-storage-sym.herokuapp.com/locations/all', headers={

    #r = requests.get('https://mirchev-home-storage-sym.herokuapp.com/users/all', headers={
    #    'Authorization': '276b08dbaa4716a310675373ad9946b54261cacd;;pesho@pesho.com;;admin',
    #})
    #jsn = r.json()
    #####################
    data = {
        'one': '1_one',
        'two': '2_two',
    }
    #json_data = json.dumps(jsn)
    json_data = json.dumps(data)
    ##return HttpResponse(json_data, content_type="application/json")
    return HttpResponse(json_data, content_type="application/json")


#>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
#>>> r.status_code
#200
#>>> r.headers['content-type']
#'application/json; charset=utf8'
#>>> r.encoding
#'utf-8'
#>>> r.text
#'{"type":"User"...'
#>>> r.json()
#{'private_gists': 419, 'total_private_repos': 77, ...}
