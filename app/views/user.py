import json
import secrets
import time
from hashlib import sha1

import bcrypt as bcrypt
from django.http import HttpResponse

from rest_framework.views import APIView

from app.models import User
from app.serializers import UserSerializer, UserLoggedSerializer
from app.utils import add_access_headers


class UserNewView(APIView):
    def post(self, req):
        data = req.data.copy()
        if 'password' in data:
            bytes = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            data['password'] = bytes.decode()

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'ok'}),
                content_type="application/json",
            ))
        else:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'not_ok'}),
                content_type="application/json",
            ))


class UserLoginView(APIView):
    def post(self, req):
        users = User.objects.filter(email=req.data['email'])

        log_user = None
        for user in users:
            log_user = user
            break

        if not log_user:
            return add_access_headers(HttpResponse(
                json.dumps({'status': ''}),
                content_type="application/json",
            ))

        if log_user:
            req_pwd = req.data['password']
            if not ( bcrypt.checkpw(req_pwd.encode(), log_user.password.encode()) ):
                return add_access_headers(HttpResponse(
                    json.dumps({'status': ''}),
                    content_type="application/json",
                ))

            sha = sha1(secrets.token_bytes(4))
            serializer_logged = UserLoggedSerializer(data={
                'created_at': int(time.time()),
                'owner': log_user.id,
                'token': sha.hexdigest()
            })

            if not serializer_logged.is_valid():
                return add_access_headers(HttpResponse(
                    json.dumps({'status': ''}),
                    content_type="application/json",
                ))

            serializer_logged.save()
            return add_access_headers(HttpResponse(
                json.dumps({
                    'status': 'ok',
                    'usrId': log_user.id,
                    'token': log_user.token,
                    'user': {
                        'id':    log_user.id,
                        'name':  log_user.name,
                        'email': log_user.email,
                        'role':  log_user.role,
                    }
                }),
                content_type="application/json",
            ))
