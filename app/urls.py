from django.urls import path

from app.views.test import test
from app.views.user import UserNewView, UserLoginView, UserDeleteView

urlpatterns = [
    path('users/new', UserNewView.as_view(), name='user-new'),
    path('user/login', UserLoginView.as_view(), name='user-login'),
    path('users/<int:id>/delete', UserDeleteView.as_view(), name='user-delete'),
    path('', test, name='test'),
]
