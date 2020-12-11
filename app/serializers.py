from rest_framework import serializers
from app.models import User, UserLogged, Location, Container, Item


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserLoggedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogged
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
