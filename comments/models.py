from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import TimeStampedModel
from movies.models import Movie


class Comment(TimeStampedModel):
    text = models.TextField(null=False, blank=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f'[Comment] id: {self.id}'

    class Meta:
        db_table = 'comments'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
