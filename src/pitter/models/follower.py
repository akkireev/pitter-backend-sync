from django.db import models

from pitter.models.base import BaseModel
from pitter.models.user import User


class Follower(BaseModel):
    target = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='targets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def follow(target: User, follower: User):
        return Follower.objects.get_or_create(target=target, follower=follower)

    @staticmethod
    def unfollow(target: User, follower: User):
        Follower.objects.filter(target=target, follower=follower).delete()

    @staticmethod
    def get_user_following_list(user):
        return [follow.target for follow in user.targets.all()]

    @staticmethod
    def get_user_followers(user):
        return [follow.follower for follow in user.followers.all()]

    @staticmethod
    def is_following_by(target, follower):
        return Follower.objects.filter(target=target, follower=follower).exists()
