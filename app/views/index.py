import json

from django.http import HttpResponse
from django.shortcuts import render

#from app.forms.profiles import ProfileForm
#from app.models import Profile, Expense
#from app.views.profiles import create_profile
from pip._vendor import requests

from app.models import User


def index(request):
    user = User
    user.name = "Kiro"
    user.email = "Peshev"
    #user.save()
    #r = requests.get('https://mirchev-home-storage-sym.herokuapp.com/locations/all', headers={
    r = requests.get('https://mirchev-home-storage-sym.herokuapp.com/users/all', headers={
        'Authorization': '276b08dbaa4716a310675373ad9946b54261cacd;;pesho@pesho.com;;admin',
    })
    jsn = r.json()
    ####################
    data = {
        'one': '1_one',
        'two': '2_two',
    }
    json_data = json.dumps(jsn)
    #return HttpResponse(json_data, content_type="application/json")
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
