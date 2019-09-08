from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import TimeStampedModel


class Movie(TimeStampedModel):
    title = models.CharField(max_length=100, null=False, blank=False, unique=True)
    year = models.CharField(max_length=4, null=True, blank=False)
    rated = models.CharField(max_length=10, null=True, blank=False)
    released = models.DateField(null=True, blank=False)
    runtime = models.CharField(max_length=10, null=True, blank=False)
    genre = models.CharField(max_length=120, null=True, blank=False)
    director = models.CharField(max_length=120, null=True, blank=False)
    writer = models.CharField(max_length=120, null=True, blank=False)
    actors = models.CharField(max_length=240, null=True, blank=False)
    plot = models.TextField(null=True, blank=False)
    language = models.CharField(max_length=120, null=True, blank=False)
    country = models.CharField(max_length=120, null=True, blank=False)
    awards = models.CharField(max_length=120, null=True, blank=False)
    poster = models.URLField(null=True, blank=False)
    metascore = models.IntegerField(null=True, blank=False)
    imdbrating = models.FloatField(null=True, blank=False)
    imdbvotes = models.IntegerField(null=True, blank=False)
    imdbid = models.CharField(max_length=120, null=True, blank=False)
    typee = models.CharField(max_length=120, null=True, blank=False)  # 'type' is build-in name
    dvd = models.DateField(null=True, blank=False)
    boxoffice = models.CharField(max_length=120, null=True, blank=False)
    production = models.CharField(max_length=120, null=True, blank=False)
    website = models.URLField(null=True, blank=False)
    response = models.BooleanField(null=True, blank=False)
    totalseasons = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'[Movie] id: {self.id}; title: {self.title}'

    class Meta:
        db_table = 'movies'
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')


class Rating(TimeStampedModel):
    source = models.CharField(max_length=120, null=True, blank=False)
    value = models.CharField(max_length=120, null=True, blank=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f'[Rating] id: {self.id}'

    class Meta:
        db_table = 'ratings'
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')
