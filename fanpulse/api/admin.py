from django.contrib import admin

# Register your models here.
from .models import Idea

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'approve', 'votes', 'username']
    # If you want to allow changing the creator in admin:
    fields = ['title', 'description', 'approve', 'votes', 'creator', 'username']
