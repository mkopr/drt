from django.contrib import admin
from django.urls import include, path

from comments.views import CommentViewSet
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from movies.views import MovieViewSet, TopView
from rest_framework import permissions, routers

schema_view = get_schema_view(
   openapi.Info(
       title='DRT API',
       default_version='v1',
       description='Decathlon Recruitment Task github.com/mkopr/drt',
       contact=openapi.Contact(email='marcinkoprek@protonmail.com'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'movies', MovieViewSet, basename='movies')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/top/', TopView.as_view()),

    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger documentation'),
]
