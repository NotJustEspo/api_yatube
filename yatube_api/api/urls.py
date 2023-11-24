from django.urls import path, include

from api.views import PostsViewSet, GroupViewSet, CommentViewSet

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'api/v1/posts', PostsViewSet)
router.register(r'api/v1/groups', GroupViewSet)
router.register(
    r'api/v1/posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('', include(router.urls), name='api-root'),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]
