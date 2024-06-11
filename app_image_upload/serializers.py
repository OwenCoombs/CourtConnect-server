from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['id', 'first_name', 'last_name', 'image']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'profile')


class CourtsSerializer(serializers.ModelSerializer):
    active_users = serializers.SerializerMethodField()

    class Meta:
        model = Courts
        fields = ('id', 'name', 'location', 'amenities', 'active_users')

    def get_active_users(self, obj):
        active_users = obj.get_active_users()
        return UserSerializer(active_users, many=True).data
    

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'court', 'active', 'timestamp']

    def create(self, validated_data):
        return Activity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

