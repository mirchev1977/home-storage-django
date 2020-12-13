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

            item = ItemSerializer(data={
                'container': serializer.data['id'],
                'description': serializer.data['description'],
                'img_url': serializer.data['url']
            })
            if item.is_valid():
                item.save()

        return add_access_headers(HttpResponse(
            json.dumps(resp),
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

        container = None
        try:
            container = Container.objects.get(pk=id)
        except:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'Container CANNOT be updated!'}),
                content_type="application/json",
            ))

        if container.creator.id != owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'Not sufficient rights for this operation!'}),
                content_type="application/json",
            ))

        data = req.data.copy()
        data['img_link'] = data['url']
        serializer = ContainerSerializer(container, data=data)
        if not serializer.is_valid():
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'Container CANNOT be updated!'}),
                content_type="application/json",
            ))

        serializer.save()

        return add_access_headers(HttpResponse(
            json.dumps({'status': 'ok', 'container': id}),
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

class ContainerSearchItemView(APIView):
    def post(self, req):
        owner_id = checkCredentials(req)

        if not owner_id:
            return add_access_headers(HttpResponse(
                json.dumps({'status': 'err', 'msg': 'User NOT logged in!'}),
                content_type="application/json",
            ))

        containers = Container.objects.filter(location_id=req.data['location'])

        location_items = []
        for cont in containers:
            itms = Item.objects.filter(container_id=cont.id)
            for itm in itms:
                location_items.append(itm)

        searchTerm = req.query_params['searchTerm']
        searchTerm = searchTerm.lower()

        found_containers = {}
        for item in location_items:
            descr = item.description
            descr = descr.lower()
            if descr.find(searchTerm) != -1:
                container = Container.objects.get(pk=item.container.id)
                found_containers[container.id] = container

        resp_arr = []
        for f_cont_key in found_containers:
            found = found_containers[f_cont_key]
            resp_arr.append({
                'id': found.id,
                'description': found.description,
                'vertical': found.vertical,
                'items': found.items,
                'privacy': found.privacy,
                'getImgLink': found.url,
                'url': found.url,
                'coords': found.coords,
                'creator': found.creator.id,
                'location': found.location.id,
            })

        resp = {'status': 'ok', 'containers': resp_arr}

        return add_access_headers(HttpResponse(
            json.dumps(resp),
            content_type="application/json",
        ))



