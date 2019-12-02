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
        return Follower.objects.filter(follower=user).all()

    @staticmethod
    def get_user_followers(user):
        return Follower.objects.filter(target=user).all()

    @staticmethod
    def get_followers_num(user):
        return Follower.objects.filter(target=user).count()

    @staticmethod
    def get_following_num(user):
        return Follower.objects.filter(follower=user).count()
