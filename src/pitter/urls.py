from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

SchemaView = get_schema_view(
    openapi.Info(title="Pitter API", default_version='v1', description="Pitter REST API"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

API_V1_URLS = [
    path('mobile/', include(('api_client.urls', 'pitter_client'), namespace='pitter_client')),
]

urlpatterns = [  # pylint: disable=invalid-name
    path('api/pitter/v1/', include((API_V1_URLS, 'pitter'), namespace='v1')),
    path('api/pitter/swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
