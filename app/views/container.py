import json
import secrets
import time
from hashlib import sha1

import bcrypt as bcrypt
from django.http import HttpResponse

from rest_framework.views import APIView

from app.models import User, UserLogged, Container
from app.serializers import UserSerializer, UserLoggedSerializer, ContainerSerializer
from app.utils import add_access_headers, checkCredentials


class ContainerNewView(APIView):
    def post(self, req):
        owner_id = checkCredentials(req)

        if not owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
                content_type="application/json",
            ))

        resp = {'status': 'err'}
        data = req.data.copy()
        data['img_link'] = data['imgLink']
        serializer = ContainerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            resp['status'] = 'ok'
            resp['contId'] = serializer.data['id']
            resp['coords'] = data['coords']

        return add_access_headers(HttpResponse(
            json.dumps(resp),
            content_type="application/json",
        ))


class ContainerLoginView(APIView):
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

class ContainerDeleteView(APIView):
    def get(self, req, id):
        owner_id = checkCredentials(req)

        if not owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
                content_type="application/json",
            ))

        container = None
        try:
            container = Container.objects.get(pk=id)
            if container.creator.id != owner_id:
                return add_access_headers(HttpResponse(
                    json.dumps({'status': 'err', 'msg': 'Container... CANNOT be deleted!'}),
                    content_type="application/json",
                ))
            container.delete()
        except:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'Not sufficient rights for this operation!'}),
                content_type="application/json",
            ))

        return add_access_headers(HttpResponse(
            json.dumps({'status': 'ok', 'id': id}),
            content_type="application/json",
        ))


class ContainerUpdateView(APIView):
    def post(self, req, id):
        owner_id = checkCredentials(req)

        if not owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
                content_type="application/json",
            ))

        user = None
        try:
            user = User.objects.get(pk=id)
        except:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User CANNOT be updated!'}),
                content_type="application/json",
            ))

        if user.role != 'admin':
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'Not sufficient rights for this operation!'}),
                content_type="application/json",
            ))

        data = req.data.copy()
        data['password'] = user.password
        serializer = UserSerializer(user, data=data)
        if not serializer.is_valid():
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User CANNOT be updated!'}),
                content_type="application/json",
            ))

        serializer.save()

        return add_access_headers(HttpResponse(
            json.dumps({'status': 'ok'}),
            content_type="application/json",
        ))

class ContainersAllView(APIView):
    def get(self, req):

        containers = Container.objects.all()

        resp = {'status': 'ok', 'containers': []}
        for cont in containers:
            resp['containers'].append({
                'id': cont.id,
                'description': cont.description,
                'vertical': cont.vertical,
                'items': cont.items,
                'privacy': cont.privacy,
                'getImgLink': cont.url,
                'url': cont.url,
                'coords': cont.coords,
                'creator': cont.creator.id,
                'location': cont.location.id,
            })

        return add_access_headers(HttpResponse(
            json.dumps(resp),
            content_type="application/json",
        ))

class ContainerLogoutView(APIView):
    def get(self, req):
        owner_id = checkCredentials(req)

        if not owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
                content_type="application/json",
            ))

        token = req.headers['authorization']
        lst_token = token.split(';;')

        tokens = UserLogged.objects.filter(token=lst_token[0])

        for tkn in tokens:
            if tkn:
                tkn.delete()

        return add_access_headers(HttpResponse(
            json.dumps({'status': 'ok'}),
            content_type="application/json",
        ))
