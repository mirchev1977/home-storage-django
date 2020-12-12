from django.urls import path

from app.views.test import test
from app.views.user import UserNewView, UserLoginView

urlpatterns = [
    path('users/new', UserNewView.as_view(), name='user-new'),
    path('user/login', UserLoginView.as_view(), name='user-login'),
    path('', test, name='test'),
]
