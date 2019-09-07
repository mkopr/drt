from django_filters import rest_framework as filters

from .models import Comment


class CommentFilter(filters.FilterSet):
    created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Comment
        fields = ['movie_id', 'created_after', 'created_before']
