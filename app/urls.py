from django.urls import path

from app.views.index import index

urlpatterns = [
    path('', index, name='index'),
]
