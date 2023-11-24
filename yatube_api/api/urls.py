from django.urls import path, include

from api.views import PostsViewSet

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'api/v1/posts', PostsViewSet, basename='posts')


urlpatterns = [
    path('', include(router.urls), name='api-root'),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]
