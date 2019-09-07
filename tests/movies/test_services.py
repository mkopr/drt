from unittest.mock import patch

from django.test import TestCase

from movies.models import Movie, Rating
from movies.services import (create_movie_object, create_rating_object,
                             format_date, get_movie_data_by_title,
                             lowercase_dict_keys, prepare_movie_data)

from .constants import movie_data, prepared_movie_data, prepared_movie_ratings


class ServicesTestCase(TestCase):

    def test_get_movie_data_by_title(self):
        downloaded_movie_data = get_movie_data_by_title(movie_data['Title'])
        self.assertEqual(downloaded_movie_data['Title'], movie_data['Title'])
        self.assertEqual(downloaded_movie_data['Year'], movie_data['Year'])
        self.assertEqual(downloaded_movie_data['Production'], movie_data['Production'])

    def text_create_movie_object(self):
        movies_before = Movie.objects.count()
        with patch('movies.services.prepare_movie_data', return_value=(prepared_movie_data, prepared_movie_ratings)):
            movie_obj = create_movie_object(movie_data)
            movies_after = Movie.objects.count()
            self.assertEqual(movie_obj.title, Movie.objects.last().title)
            self.assertNotEqual(movies_before, movies_after)

    def test_prepare_movie_data(self):
        test_prepared_movie_data, test_prepared_movie_ratings = prepare_movie_data(movie_data)
        self.assertEqual(test_prepared_movie_data, prepared_movie_data)

        self.assertEqual(test_prepared_movie_ratings[0]['source'], prepared_movie_ratings[0]['source'])
        self.assertEqual(test_prepared_movie_ratings[0]['value'], prepared_movie_ratings[0]['value'])
        self.assertEqual(test_prepared_movie_ratings[1]['source'], prepared_movie_ratings[1]['source'])
        self.assertEqual(test_prepared_movie_ratings[1]['value'], prepared_movie_ratings[1]['value'])

    def test_create_rating_object(self):
        ratings_before = Rating.objects.count()
        movie = Movie.objects.create(title='title1')
        ratings = create_rating_object(prepared_movie_ratings, movie)
        self.assertEqual(len(prepared_movie_ratings), len(ratings))
        ratings_after = Rating.objects.count()
        self.assertNotEqual(ratings_before, ratings_after)

    def test_lowercase_dict_keys(self):
        lowercase_movie_data = lowercase_dict_keys(movie_data)
        for key, value in lowercase_movie_data.items():
            self.assertTrue(key.islower())

    def test_format_date(self):
        date = movie_data['DVD']
        new_date = format_date(date)
        self.assertNotEqual(date, new_date)
        self.assertTrue('-' in new_date)
