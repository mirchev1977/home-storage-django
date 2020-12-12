import json
import secrets
import time
from hashlib import sha1

import bcrypt as bcrypt
from django.http import HttpResponse

from rest_framework.views import APIView

from app.models import User, UserLogged, Location
from app.serializers import UserSerializer, UserLoggedSerializer, LocationSerializer
from app.utils import add_access_headers, checkCredentials


#class UserNewView(APIView):
#    def post(self, req):
#        data = req.data.copy()
#        if 'password' in data:
#            bytes = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
#            data['password'] = bytes.decode()
#
#        serializer = UserSerializer(data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return add_access_headers(HttpResponse(
#                json.dumps({'status': 'ok'}),
#                content_type="application/json",
#            ))
#        else:
#            return add_access_headers(HttpResponse(
#                json.dumps({'status': 'not_ok'}),
#                content_type="application/json",
#            ))


#class UserLoginView(APIView):
#    def post(self, req):
#        users = User.objects.filter(email=req.data['email'])
#
#        log_user = None
#        for user in users:
#            log_user = user
#            break
#
#        if not log_user:
#            return add_access_headers(HttpResponse(
#                json.dumps({'status': ''}),
#                content_type="application/json",
#            ))
#
#        if log_user:
#            req_pwd = req.data['password']
#            if not ( bcrypt.checkpw(req_pwd.encode(), log_user.password.encode()) ):
#                return add_access_headers(HttpResponse(
#                    json.dumps({'status': ''}),
#                    content_type="application/json",
#                ))
#
#            sha = sha1(secrets.token_bytes(4))
#            serializer_logged = UserLoggedSerializer(data={
#                'created_at': int(time.time()),
#                'owner': log_user.id,
#                'token': sha.hexdigest()
#            })
#
#            if not serializer_logged.is_valid():
#                return add_access_headers(HttpResponse(
#                    json.dumps({'status': ''}),
#                    content_type="application/json",
#                ))
#
#            serializer_logged.save()
#            return add_access_headers(HttpResponse(
#                json.dumps({
#                    'status': 'ok',
#                    'usrId': log_user.id,
#                    'token': log_user.token,
#                    'user': {
#                        'id':    log_user.id,
#                        'name':  log_user.name,
#                        'email': log_user.email,
#                        'role':  log_user.role,
#                    }
#                }),
#                content_type="application/json",
#            ))

#class UserDeleteView(APIView):
#    def get(self, req, id):
#        owner_id = checkCredentials(req)
#
#        if not owner_id:
#            return add_access_headers(HttpResponse(
#                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
#                content_type="application/json",
#            ))
#
#        if owner_id != id:
#            return add_access_headers(HttpResponse(
#                json.dumps({'status': 'err', 'msg': 'User CANNOT be deleted!'}),
#                content_type="application/json",
#            ))
#
#        user = None
#        try:
#            user = User.objects.get(pk=id)
#        except:
#            return add_access_headers(HttpResponse(
#                json.dumps({'status': 'err', 'msg': 'User... CANNOT be deleted!'}),
#                content_type="application/json",
#            ))
#
#        if user.role != 'admin':
#            return add_access_headers(HttpResponse(
#                json.dumps({'status': 'err', 'msg': 'Not sufficient rights for this operation!'}),
#                content_type="application/json",
#            ))
#
#        user.delete()
#
#        return add_access_headers(HttpResponse(
#            json.dumps({'status': 'ok', 'userId': id}),
#            content_type="application/json",
#        ))


class LocationUpdateView(APIView):
    def post(self, req, id):
        owner_id = checkCredentials(req)

        if not owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
                content_type="application/json",
            ))

        data = req.data.copy()
        data['img_url'] = data['imgUrl']
        if id and id > 0:
            data['id'] = id
            loc = Location.objects.get(pk=id)
            serializer = LocationSerializer(loc, data=data)
        else:
            data['id'] = 0
            serializer = LocationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

        resp = {
            'status': 'ok',
            'cont': serializer.data,
            'locId': serializer.data['id'],
            'usrId': serializer.data['creator'],
            'contCreator': serializer.data['creator'],
            'creator': serializer.data['creator'],
        }

        return add_access_headers(HttpResponse(
            json.dumps(resp),
            content_type="application/json",
        ))

#class UsersAllView(APIView):
#    def get(self, req):
#        owner_id = checkCredentials(req)
#
#        if not owner_id:
#            return add_access_headers(HttpResponse(
#                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
#                content_type="application/json",
#            ))
#
#        users = User.objects.all()
#
#        resp = {'status': 'ok', 'users': []}
#        for usr in users:
#            resp['users'].append({
#                'id': usr.id,
#                'name': usr.name,
#                'email': usr.email,
#                'password': usr.password,
#                'role': usr.role,
#                'token': usr.token,
#            })
#
#        return add_access_headers(HttpResponse(
#            json.dumps(resp),
#            content_type="application/json",
#        ))

#class UserLogoutView(APIView):
#    def get(self, req):
#        owner_id = checkCredentials(req)
#
#        if not owner_id:
#            return add_access_headers(HttpResponse(
#                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
#                content_type="application/json",
#            ))
#
#        token = req.headers['authorization']
#        lst_token = token.split(';;')
#
#        tokens = UserLogged.objects.filter(token=lst_token[0])
#
#        for tkn in tokens:
#            if tkn:
#                tkn.delete()
#
#        return add_access_headers(HttpResponse(
#            json.dumps({'status': 'ok'}),
#            content_type="application/json",
#        ))
