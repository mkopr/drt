from django.db.models import Count

from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .filters import MovieFilter
from .models import Movie
from .serializers import (CreateMovieSerializer, MovieSerializer,
                          TopDatesSerializer, TopSerializer,
                          UpdateMovieSerializer)
from .services import (calculate_rank, create_movie_object,
                       get_movie_data_by_title)


class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows movies to be viewed, created, edited or deleted.
    Order response by released, imdbrating, imdbvotes, dvd; example: ?ordering=released
    Filter response by typee, genre, min_year, max_year; example: ?min_year=2049
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = MovieFilter
    ordering_fields = ['released', 'imdbrating', 'imdbvotes', 'dvd']

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateMovieSerializer
        if self.action == 'update':
            return UpdateMovieSerializer
        return MovieSerializer

    @swagger_auto_schema(responses={200: MovieSerializer(many=True)})
    def create(self, request):
        serialized = self.get_serializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        title = serialized.validated_data.get('title', None)
        if title:
            data = dict(get_movie_data_by_title(title))
            movie = create_movie_object(data)
            serialized = MovieSerializer(movie)
            return Response(serialized.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TopView(views.APIView):
    """
    API endpoint that allows top to be viewed.
    Add total_comments field in queryset and order by it.
    Filter by created_before (required) and created_after (required); example: ?created_before=2001&created_after=1977
    """

    @swagger_auto_schema(responses={200: TopSerializer(many=True)})
    def get(self, request):
        serialized = TopDatesSerializer(data=request.query_params)
        serialized.is_valid(raise_exception=True)
        queryset = Movie.objects.all().filter(
            comment__created_at__lte=serialized.data.get('created_before'),
            comment__created_at__gte=serialized.data.get('created_after')
        ).annotate(total_comments=Count('comment')).order_by('-total_comments')
        queryset = calculate_rank(queryset)
        serialized = TopSerializer(queryset, many=True)
        return Response(serialized.data)
