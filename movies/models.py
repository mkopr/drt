from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import TimeStampedModel


class Movie(TimeStampedModel):
    title = models.CharField(max_length=100, null=False, blank=False, unique=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    rated = models.CharField(max_length=10, null=True, blank=True)
    released = models.DateField(null=True, blank=True)
    runtime = models.CharField(max_length=10, null=True, blank=True)
    genre = models.CharField(max_length=240, null=True, blank=True)
    director = models.CharField(max_length=240, null=True, blank=True)
    writer = models.TextField(null=True, blank=True)
    actors = models.CharField(max_length=240, null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=240, null=True, blank=True)
    country = models.CharField(max_length=240, null=True, blank=True)
    awards = models.CharField(max_length=240, null=True, blank=True)
    poster = models.URLField(null=True, blank=True)
    metascore = models.IntegerField(null=True, blank=True)
    imdbrating = models.FloatField(null=True, blank=True)
    imdbvotes = models.IntegerField(null=True, blank=True)
    imdbid = models.CharField(max_length=240, null=True, blank=True)
    typee = models.CharField(max_length=240, null=True, blank=True)  # 'type' is build-in name
    dvd = models.DateField(null=True, blank=True)
    boxoffice = models.CharField(max_length=240, null=True, blank=True)
    production = models.CharField(max_length=240, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    response = models.BooleanField(null=True, blank=True)
    totalseasons = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'[Movie] id: {self.id}; title: {self.title}'

    def save(self, *args, **kwargs):
        if self.metascore == '':
            self.metascore = None
        if self.imdbrating == '':
            self.imdbrating = None
        if self.imdbvotes == '':
            self.imdbvotes = None
        if self.totalseasons == '':
            self.totalseasons = None
        if self.released == '':
            self.released = None
        if self.dvd == '':
            self.dvd = None
        super(Movie, self).save(*args, **kwargs)

    class Meta:
        db_table = 'movies'
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')


class Rating(TimeStampedModel):
    source = models.CharField(max_length=240, null=True, blank=False)
    value = models.CharField(max_length=240, null=True, blank=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f'[Rating] id: {self.id}'

    class Meta:
        db_table = 'ratings'
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')
