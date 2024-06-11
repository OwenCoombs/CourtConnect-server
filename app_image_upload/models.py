from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  first_name = models.TextField()
  last_name = models.TextField()
  image = models.ImageField(upload_to='images/')

  def __str__(self):
    return self.user.username
  

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, related_name='images', on_delete=models.CASCADE, default='1')  # ForeignKey to associate image with profile

    def __str__(self):
        return self.image.name
    


class Courts(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=175)
    amenities = models.TextField()
    active_users = models.ManyToManyField(User, through='Activity', related_name='active_courts')

    def __str__(self):
        return self.name

    def get_active_users(self):
        return self.active_users.filter(activity__active=True).distinct()

    def is_user_active(self, user):
        return self.get_active_users().filter(pk=user.pk).exists()


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    court = models.ForeignKey(Courts, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} at {self.court.name} - {'Active' if self.active else 'Inactive'}"
