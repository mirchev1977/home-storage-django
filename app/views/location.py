import json

from django.http import HttpResponse

from rest_framework.views import APIView

from app.models import Location
from app.serializers import LocationSerializer
from app.utils import add_access_headers, checkCredentials


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

class LocationsAllView(APIView):
    def get(self, req):

        locations = Location.objects.all()

        resp = []
        for loc in locations:
            resp.append({
                'id': loc.id,
                'creator': loc.creator.id,
                'imgUrl': loc.img_url,
                'location': loc.location,
                'privacy': loc.privacy,
            })

        return add_access_headers(HttpResponse(
            json.dumps(resp),
            content_type="application/json",
        ))

