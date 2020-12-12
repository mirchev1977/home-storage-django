from django.urls import path

from app.views.location import LocationUpdateView
from app.views.test import test
from app.views.user import UserNewView, UserLoginView, UserDeleteView, UserUpdateView, UsersAllView, UserLogoutView

urlpatterns = [
    #user routes
    path('users/new', UserNewView.as_view(), name='user-new'),
    path('user/login', UserLoginView.as_view(), name='user-login'),
    path('users/<int:id>/delete', UserDeleteView.as_view(), name='user-delete'),
    path('users/<int:id>/update', UserUpdateView.as_view(), name='user-update'),
    path('users/all', UsersAllView.as_view(), name='user-all'),
    path('user/logout', UserLogoutView.as_view(), name='user-logout'),

    #location routes
    path('locations/<int:id>/update', LocationUpdateView.as_view(), name='location-update'),

    #test
    path('', test, name='test'),
]
