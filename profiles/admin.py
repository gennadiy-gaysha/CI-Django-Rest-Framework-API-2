from django.contrib import admin
from .models import Profile

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('owner', 'created_at', 'name', 'content', 'image')
#     search_fields = ('owner',)

# admin.site.register(Profile, ProfileAdmin)

admin.site.register(Profile)
