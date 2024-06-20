from django.contrib import admin
from app_image_upload.models import *


class ProfileAdmin(admin.ModelAdmin):
  pass


class ImageAdmin(admin.ModelAdmin):
  pass

class CourtsAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'amenities')
    search_fields = ('name', 'location', 'amenities')  # Include amenities in search
    list_filter = ('location',)  # Add location as a filter option


class ActivityAdmin(admin.ModelAdmin):
   pass

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Courts, CourtsAdmin)
admin.site.register(Activity, ActivityAdmin)