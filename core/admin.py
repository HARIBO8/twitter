from django.contrib import admin
from .models import Profile, Follow, Tweet

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Tweet)