from django.db import models

from pitter.models.user import User


class Follower(models.Model):
    target = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='targets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)