import json
from datetime import timedelta
from unittest.mock import patch

from comments.models import Comment
from movies.models import Movie
from rest_framework.test import APITestCase

from .constants import movie_data


class MovieViewSetTestCase(APITestCase):
    url = '/api/movies/'

    def setUp(self):
        self.movie1 = Movie.objects.create(title='movie title 1', imdbvotes=200, typee='A')
        self.movie2 = Movie.objects.create(title='movie title 2', imdbvotes=300, typee='B')
        self.movie3 = Movie.objects.create(title='movie title 3', imdbvotes=400, typee='C')

    def test_get_movie(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(json.loads(response.content)['count'] == Movie.objects.count())

    def test_get_movie_ordering(self):
        response = self.client.get(self.url, {'ordering': '-imdbvotes'})
        self.assertEqual(200, response.status_code)

        results = json.loads(response.content)['results']
        highest_imdbvotes = self.movie3.imdbvotes
        for result in results:
            self.assertTrue(highest_imdbvotes >= result['imdbvotes'])
            highest_imdbvotes = result['imdbvotes']

    def test_get_movie_filtering(self):
        for movie in Movie.objects.all():
            response = self.client.get(self.url, {'typee': movie.typee})
            self.assertEqual(200, response.status_code)
            self.assertEqual(json.loads(response.content)['results'][0]['title'], movie.title)

    def test_create_movie(self):
        title = 'Interstelar'
        with patch('movies.services.get_movie_data_by_title', return_value=movie_data):
            response = self.client.post(self.url, {"title": title})
            self.assertEqual(200, response.status_code)
            self.assertEqual(title, json.loads(response.content)['title'])

    def test_invalid_create_movie(self):
        response = self.client.post(self.url)
        self.assertEqual(400, response.status_code)

    def test_update_movie(self):
        new_title = 'edited movie title 1'
        url = f'{self.url}{str(self.movie1.id)}/'
        response = self.client.put(url, {'title': new_title})
        self.assertEqual(200, response.status_code)
        self.assertEqual(new_title, json.loads(response.content)['title'])

        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(new_title, json.loads(response.content)['title'])

    def test_delete_movie(self):
        url = f'{self.url}{str(self.movie1.id)}/'
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)

        response = self.client.get(url)
        self.assertEqual(404, response.status_code)


class TopViewTestCase(APITestCase):
    url = '/api/top/'

    def setUp(self):
        self.movie1 = Movie.objects.create(title='movie title 1')
        self.movie2 = Movie.objects.create(title='movie title 2')
        self.movie3 = Movie.objects.create(title='movie title 3')

        self.comment1 = Comment.objects.create(text='text1', movie=self.movie1)
        self.comment2 = Comment.objects.create(text='text2', movie=self.movie1)
        self.comment3 = Comment.objects.create(text='text3', movie=self.movie2)
        self.comment4 = Comment.objects.create(text='text4', movie=self.movie3)

    def test_get_top(self):
        response = self.client.get(
            self.url,
            {
                'created_before': str(self.comment1.created_at.date()),
                'created_after': str(self.comment1.created_at.date() - timedelta(days=1))
            }
        )
        self.assertTrue(200, response.status_code)

    def test_invalid_get_top(self):
        response = self.client.get(self.url)
        self.assertTrue(400, response.status_code)
