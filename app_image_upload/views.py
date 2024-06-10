from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework import viewsets


from .models import *
from .serializers import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
  user = request.user
  profile = user.profile
  serializer = ProfileSerializer(profile, many=False)
  return Response(serializer.data)


@api_view(['POST'])
@permission_classes([])
def create_user(request):
    user = User.objects.create(
        username = request.data['username'],
        password = request.data['password']
    )
    user.save()
    profile = Profile.objects.create(
        user = user,
        first_name = request.data['first_name'],
        last_name = request.data['last_name']
    )
    profile.save()
    profile_serialized = ProfileSerializer(profile)
    return Response(profile_serialized.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def create_image(request):
    user_profile = request.user.profile
    image_serialized = ImageSerializer(data=request.data)  # Use ImageSerializer instead of ProfileSerializer
    if image_serialized.is_valid():
        # Associate the image with the user's profile
        image_serialized.save(profile=user_profile)
        return Response(image_serialized.data, status=status.HTTP_201_CREATED)
    return Response(image_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

   


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_images(request):
    user = request.user
    user_images = Image.objects.filter(profile__user=user)
    serialized_images = ImageSerializer(user_images, many=True)
    return Response(serialized_images.data)
