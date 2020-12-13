import json
import secrets
import time
from hashlib import sha1

import bcrypt as bcrypt
from django.http import HttpResponse

from rest_framework.views import APIView

from app.models import User, UserLogged, Container, Item
from app.serializers import UserSerializer, UserLoggedSerializer, ContainerSerializer, ItemSerializer
from app.utils import add_access_headers, checkCredentials


class ItemNewView(APIView):
    def post(self, req):
        owner_id = checkCredentials(req)

        if not owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
                content_type="application/json",
            ))

        resp = {'status': 'err'}
        data = req.data.copy()
        data['img_url'] = data['imgUrl']
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            resp['status'] = 'ok'
            resp['id'] = serializer.data['id']

        return add_access_headers(HttpResponse(
            json.dumps(resp),
            content_type="application/json",
        ))


class ItemDeleteView(APIView):
    def get(self, req, id):
        owner_id = checkCredentials(req)

        if not owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
                content_type="application/json",
            ))

        item = None
        try:
            item = Item.objects.get(pk=id)
            item.delete()
        except:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'Not sufficient rights for this operation!'}),
                content_type="application/json",
            ))

        return add_access_headers(HttpResponse(
            json.dumps({'status': 'ok', 'id': id}),
            content_type="application/json",
        ))


class ItemUpdateView(APIView):
    def post(self, req, id):
        owner_id = checkCredentials(req)

        if not owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
                content_type="application/json",
            ))

        resp = {'status': 'err'}
        data = req.data.copy()
        data['img_url'] = data['imgUrl']

        item = Item.objects.get(pk=id)

        serializer = ItemSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            resp['status'] = 'ok'
            resp['id'] = serializer.data['id']

        return add_access_headers(HttpResponse(
            json.dumps(resp),
            content_type="application/json",
        ))

class ItemsAllView(APIView):
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

