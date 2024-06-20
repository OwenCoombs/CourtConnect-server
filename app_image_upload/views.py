from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.utils import timezone  # Add this import statement
import logging
from .models import *
from .serializers import *

logger = logging.getLogger(__name__)

# View to get profile details of the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = user.profile
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)

# View to create a new user
@api_view(['POST'])
@permission_classes([])
def create_user(request):
    # Extract data from request and create a new user and profile
    user = User(
        username=request.data['username']
    )
    user.set_password(request.data['password'])
    user.save()

    profile = Profile.objects.create(
        user=user,
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )
    profile.save()

    profile_serialized = ProfileSerializer(profile)
    return Response(profile_serialized.data)

# View to create a new image associated with the authenticated user's profile
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

# View to get all images uploaded by the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_images(request):
    user = request.user
    user_images = Image.objects.filter(profile__user=user)
    serializer = ImageSerializer(user_images, many=True)
    return Response(serializer.data)

# View to get all images
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_images(request):
    images = Image.objects.all()
    images_serialized = ImageSerializer(images, many=True)
    return Response(images_serialized.data)

# View to delete a specific post (image)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    try:
        post = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        return Response({'error': 'Post not found'})
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# View to search and get courts based on provided name and/or location
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

# View to create a new court
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_court(request):
    serializer = CourtsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to set a user as active or inactive in a court
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_active_user(request):
    user = request.user
    court_id = request.data.get('court_id')
    court = Courts.objects.get(pk=court_id)
    active = False
    print('BLAMMO: COURT: ', court)
    print('BLAMMO: USER: ', user.username)
    print('BLAMMO: ACTIVE USERS: ', court.active_users.last().username)
    try:
        # get activity
        activity, created = Activity.objects.get_or_create(user=user, court=court)
        for active_user in court.active_users.all():
            if user.username == active_user.username:
                if activity.active == True:
                    active = True
        # if active we want to deactivate
        if active == True:
            print('BLAMMO: ACTIVITY IS TRUE, REMOVE THE USER')
            activity.active = False
        # else activate
        else:
            print('BLAMMO: ACTIVITY IS FALSE: ADD THE USERd')
            activity.active = True
        # save activity
        activity.save()
        return Response({"message": "Success!"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)





    # print(f"User {user.username} is trying to {'activate' if active else 'deactivate'} on court {court_id}")

    # if court_id is None or active is None:
    #     print("Court ID and active status are required.")
    #     return Response({"error": "Court ID and active status are required."}, status=status.HTTP_400_BAD_REQUEST)

    # try:
    #     court = Courts.objects.get(pk=court_id)
    # except Courts.DoesNotExist:
    #     print(f"Court with ID {court_id} not found.")
    #     return Response({"error": "Court not found."}, status=status.HTTP_404_NOT_FOUND)
    # except Exception as e:
    #     print(f"Error fetching court: {e}")
    #     return Response({"error": "An error occurred while fetching the court."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # if active == True:  # Check if the user should be activated
    #     try:
    #         activity, created = Activity.objects.get_or_create(user=user, court=court)
    #         print(f"Activity object: {activity}, Created: {created}, User: {activity.user}")
    #         if activity.active:
    #             print("User is already active at this court.")
    #             return Response({"error": "User is already active at this court."}, status=status.HTTP_400_BAD_REQUEST)
    #         activity.active = True
    #         activity.save()
            
    #         return Response({"message": "User activated successfully."}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         print(f"Error activating user: {e}")
    #         return Response({"error": "An error occurred while activating the user."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # elif active == False:  # Check if the user should be deactivated
    #     try:
    #         print('BLAMMO: ACTIVE: ', active)
    #         print('BLAMMO: COURT: ', court)
    #         print('BLAMMO: USER: ', user)
    #         activity = Activity.objects.get(user=user, court=court, active=True)
    #         activity.active = False
    #         print('USER was active but now we have deactivated them.')
    #         activity.save()
    #         return Response({"message": "User deactivated successfully."}, status=status.HTTP_200_OK)
    #     except Activity.DoesNotExist:
    #         print("User is not active at this court.")
    #         return Response({"error": "User is not active at this court."}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         print(f"Error deactivating user: {e}")
    #         return Response({"error": "An error occurred while deactivating the user."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to get all active users
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_users(request):
    try:
        active_users = Activity.objects.filter(active=True).select_related('user', 'court')
        serializer = ActivitySerializer(active_users, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error("Error in get_active_users:", exc_info=True)
        return Response({"error": "An error occurred while fetching active users."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to get reviews for a specific court
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_court_reviews(request, pk):
    try:
        court = Courts.objects.get(pk=pk)
        reviews = court.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Courts.DoesNotExist:
        return Response({"error": "Court not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error fetching court reviews: {e}")
        return Response({"error": "An error occurred while fetching court reviews."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to add a review for a specific court
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_court_review(request, pk):
    try:
        court = Courts.objects.get(pk=pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, court=court)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Courts.DoesNotExist:
        return Response({"error": "Court not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error adding court review: {e}")
        return Response({"error": "An error occurred while adding court review."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

