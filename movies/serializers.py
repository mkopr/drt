from comments.serializers import CommentSerializer
from rest_framework import serializers

from .models import Movie, Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['source', 'value']


class MovieSerializer(serializers.ModelSerializer):
    rating_set = RatingSerializer(many=True)
    comment_set = CommentSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'year', 'rated', 'released', 'runtime',
            'genre', 'director', 'writer', 'actors', 'plot', 'language',
            'country', 'awards', 'poster', 'metascore', 'imdbrating',
            'imdbvotes', 'imdbid', 'typee', 'dvd', 'boxoffice', 'production',
            'website', 'response', 'rating_set', 'comment_set'
        ]


class UpdateMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CreateMovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=True)


class TopSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField(source='id')
    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()


class TopDatesSerializer(serializers.Serializer):
    created_before = serializers.DateField(required=True)
    created_after = serializers.DateField(required=True)
