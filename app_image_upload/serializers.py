from rest_framework import serializers
from .models import *

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

# Serializer for the Profile model
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Include user serializer

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'image', 'user']

# Serializer for the Image model
class ImageSerializer(serializers.ModelSerializer):
    uploader_username = serializers.ReadOnlyField(source='profile.user.username')  # Read-only field for uploader's username

    class Meta:
        model = Image
        fields = ['id', 'image', 'title', 'desc', 'profile', 'uploader_username']

# Serializer for the Courts model
class CourtsSerializer(serializers.ModelSerializer):
    active_users = serializers.SerializerMethodField()  # Custom serializer method field for active users
    class Meta:
        model = Courts
        fields = ('id', 'name', 'location', 'amenities', 'active_users')

    # Method to get active users for a court
    def get_active_users(self, obj):
        active_users = obj.get_active_users()
        print('BLAMMO: SERIALIZERS: ACTIVE USERS: ', active_users)
        return UserSerializer(active_users, many=True).data

# Serializer for the Activity model
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'court', 'active', 'timestamp']

    # Custom create method to create an Activity object
    def create(self, validated_data):
        return Activity.objects.create(**validated_data)

    # Custom update method to update an existing Activity object
    def update(self, instance, validated_data):
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance





class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'court_id', 'rating', 'comment']
