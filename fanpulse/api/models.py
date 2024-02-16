from django.db import models
from django.conf import settings
# Create your models here.

# myapp/models.py

from django.db import models
from django.contrib.auth import get_user_model

class Idea(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    username = models.CharField(max_length=125)
    votes = models.IntegerField(default=0)  # Tracks the net votes
    approve = models.BooleanField(default=False)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # This references the currently active user model
        on_delete=models.CASCADE,  # If the user is deleted, delete their ideas too
        related_name='ideas'  # Allows us to access a user's ideas with user.ideas
    )

class Vote(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_votes')
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='idea_votes')

    class Meta:
        unique_together = ('user', 'idea')