from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import PostsViewSet, GroupViewSet, CommentsViewSet


v1_router = DefaultRouter()
v1_router.register(
    r'posts',
    PostsViewSet,
    basename='posts'
)
v1_router.register(
    r'groups',
    GroupViewSet,
    basename='groups'
)
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(v1_router.urls), name='api-root'),
    path('api-token-auth/', views.obtain_auth_token),
]
