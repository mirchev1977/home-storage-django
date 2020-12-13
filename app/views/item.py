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
    def get(self, req, contId):
        owner_id = checkCredentials(req)

        if not owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
                content_type="application/json",
            ))

        matched = []
        non_matched = []
        items = Item.objects.filter(container_id=contId)
        searchTerm = req.query_params['searchTerm']

        for item in items:
            descr = item.description
            descr = descr.lower()
            if descr.find(searchTerm) != -1:
                matched.append({
                    'id': item.id,
                    'description': item.description,
                    'imgUrl': item.img_url,
                    'contId': contId,
                })
            else:
                non_matched.append({
                    'id': item.id,
                    'description': item.description,
                    'imgUrl': item.img_url,
                    'contId': contId,
                })

        joined_items = matched + non_matched

        resp = {'status': 'ok', 'contId': contId, 'items': joined_items}

        return add_access_headers(HttpResponse(
            json.dumps(resp),
            content_type="application/json",
        ))

class ItemsPasteView(APIView):
    def get(self, req):
        owner_id = checkCredentials(req)

        if not owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
                content_type="application/json",
            ))

        data = req.data.copy()
        paste_items = data['itemIds']

        for itemId in paste_items:
            item = Item.objects.get(pk=itemId)
            item_data = {
                'description': item.description,
                'img_url': item.img_url,
                'container_id': itemId
            }
            serializer = ItemSerializer(item, data=item_data)
            if serializer.is_valid():
                serializer.save()

        return add_access_headers(HttpResponse(
            json.dumps({'status': 'ok'}),
            content_type="application/json",
        ))
