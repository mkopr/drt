from comments.models import Comment
from comments.serializers import CommentSerializer
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .filters import CommentFilter


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or created.
    Order response by movie_id, created_at; ?ordering=movie_id
    Filter response by movie_id, created_after, created_before; ?created_before=1984
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = CommentFilter
    ordering_fields = ['movie_id', 'created_at']

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
