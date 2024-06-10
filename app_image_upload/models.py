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
