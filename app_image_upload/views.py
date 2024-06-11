from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from .models import *
from .serializers import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = user.profile
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_image(request):
    user_profile = request.user.profile
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(profile=user_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_images(request):
    user = request.user
    user_images = Image.objects.filter(profile__user=user)
    serializer = ImageSerializer(user_images, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_court(request):
    name = request.GET.get('name')
    location = request.GET.get('location')

    filter_conditions = {}
    if name:
        filter_conditions['name__icontains'] = name
    if location:
        filter_conditions['location__icontains'] = location

    courts = Courts.objects.filter(**filter_conditions)
    serializer = CourtsSerializer(courts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_court(request):
    serializer = CourtsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_active_user(request):
    user = request.user
    court_id = request.data.get('court_id')
    active = request.data.get('active')

    if court_id is None:
        return Response({"error": "Court ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        court = Courts.objects.get(pk=court_id)
    except Courts.DoesNotExist:
        return Response({"error": "Court not found."}, status=status.HTTP_404_NOT_FOUND)

    if active:
        # Check if the user is already active at this court
        activity, created = Activity.objects.get_or_create(user=user, court=court)
        if activity.active:
            return Response({"error": "User is already active at this court."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            activity.active = True
            activity.save()
            return Response({"message": "User activated successfully."}, status=status.HTTP_200_OK)
    else:
        # Deactivate the user's active status at the court
        try:
            activity = Activity.objects.get(user=user, court=court, active=True)
            activity.active = False
            activity.save()
            return Response({"message": "User deactivated successfully."}, status=status.HTTP_200_OK)
        except Activity.DoesNotExist:
            return Response({"error": "User is not active at this court."}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_users(request):
    try:
        # Query active users based on your application logic
        active_users = Activity.objects.filter(active=True)

        # Serialize the active users data
        serializer = ActivitySerializer(active_users, many=True)

        # Return the serialized data in the HTTP response
        return Response(serializer.data)
    except Exception as e:
        # Log any exceptions that occur during the execution of the view function
        print("Error in get_active_users:", e)
        return Response({"error": "An error occurred while fetching active users."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
