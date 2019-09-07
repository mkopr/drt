from django.contrib import admin

from movies.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Basic implementation of Movie model for admin panel.
    """
    search_fields = (
        'id', 'title', 'released'
    )
    list_filter = ('typee', 'genre', 'year')
