from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Add this import statement

# Profile model to extend the built-in User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.TextField()
    last_name = models.TextField()
    image = models.ImageField(upload_to='images/')  # ImageField for user profile picture

    def __str__(self):
        return self.user.username  # String representation of the profile object


# Image model to store uploaded images
class Image(models.Model):
    image = models.ImageField(upload_to='images/')  # ImageField for the uploaded image
    uploaded_at = models.DateTimeField(auto_now_add=True)  # DateTimeField for the upload timestamp
    profile = models.ForeignKey(Profile, related_name='images', on_delete=models.CASCADE, default='1')  # ForeignKey to associate image with profile
    title = models.TextField(default='')  # TextField for image title
    desc = models.TextField(default='')  # TextField for image description

    def __str__(self):
        return self.title  # String representation of the image object


# Courts model to represent sports courts
class Courts(models.Model):
    name = models.CharField(max_length=50)  # CharField for court name
    location = models.CharField(max_length=175)  # CharField for court location
    amenities = models.TextField()  # TextField for court amenities
    active_users = models.ManyToManyField(User, through='Activity', related_name='active_courts')  # Many-to-many relationship with User model through Activity

    def __str__(self):
        return self.name  # String representation of the court object

    # Method to get active users for a court
    def get_active_users(self):
        return self.active_users.filter(activity__active=True).distinct()

    # Method to check if a user is active in a court
    def is_user_active(self, user):
        return self.get_active_users().filter(pk=user.pk).exists()


# Activity model to track user activity in courts
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User model
    court = models.ForeignKey('Courts', on_delete=models.CASCADE)  # ForeignKey to Courts model
    active = models.BooleanField(default=False)  # BooleanField to indicate user activity status
    timestamp = models.DateTimeField(default=timezone.now)  # Updated timestamp field

    class Meta:
        unique_together = ('user', 'court')  # Ensure uniqueness for each user-court combination

    def __str__(self):
        return f"{self.user.username} at {self.court.name} - {'Active' if self.active else 'Inactive'}"  # String representation of the activity object


# Review model to store reviews for courts
class Review(models.Model):
    court = models.ForeignKey(Courts, on_delete=models.CASCADE, related_name='reviews')  # ForeignKey to Courts model
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User model
    rating = models.IntegerField()  # IntegerField for rating
    comment = models.TextField()  # TextField for review comment

    def __str__(self):
        return f"Review by {self.user.username} for {self.court.name}"  # String representation of the review object


