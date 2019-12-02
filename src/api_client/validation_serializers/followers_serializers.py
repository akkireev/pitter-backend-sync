from rest_framework import serializers


class FollowersPostRequest(serializers.Serializer):
    following_user_id = serializers.CharField(required=True, max_length=64,
                                              label='Id пользователя, на которого подписываемся')


class FollowersPostResponse(serializers.Serializer):
    pass
