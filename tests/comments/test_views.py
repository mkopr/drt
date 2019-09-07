import json

from comments.models import Comment
from movies.models import Movie
from rest_framework.test import APITestCase


class CommentViewSetTestCase(APITestCase):
    url = '/api/comments/'

    def setUp(self):
        self.movie1 = Movie.objects.create(title='movie title 1')
        self.movie2 = Movie.objects.create(title='movie title 2')
        self.movie3 = Movie.objects.create(title='movie title 3')

        self.comment1 = Comment.objects.create(text='text1', movie=self.movie1)
        self.comment2 = Comment.objects.create(text='text2', movie=self.movie1)
        self.comment3 = Comment.objects.create(text='text3', movie=self.movie2)
        self.comment4 = Comment.objects.create(text='text4', movie=self.movie3)

    def test_get_comment(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(json.loads(response.content)['count'] == Comment.objects.count())

    def test_get_comment_ordering(self):
        response = self.client.get(self.url, {'ordering': 'movie_id'})
        self.assertEqual(200, response.status_code)

        results = json.loads(response.content)['results']
        movie_id = self.comment1.movie.id
        for result in results:
            self.assertTrue(movie_id <= result['movie'])
            movie_id = result['movie']

    def test_get_comment_filtering(self):
        for comment in Comment.objects.all():
            response = self.client.get(self.url, {'movie_id': comment.movie.id})
            self.assertEqual(200, response.status_code)
            for result in json.loads(response.content)['results']:
                self.assertEqual(result['movie'], comment.movie.id)

    def test_create_comment(self):
        text = 'text5'
        response = self.client.post(self.url, {'text': text, 'movie': self.movie3.id})
        self.assertEqual(201, response.status_code)
        self.assertEqual(text, json.loads(response.content)['text'])

        response = self.client.get(f'{self.url}{Comment.objects.last().id}/')
        self.assertEqual(200, response.status_code)
        self.assertTrue(json.loads(response.content)['movie'] == self.movie3.id)

    def test_invalid_create_comment(self):
        response = self.client.post(self.url)
        self.assertEqual(400, response.status_code)

    def test_update_comment(self):
        response = self.client.put(self.url)
        self.assertEqual(405, response.status_code)

    def test_destroy_comment(self):
        response = self.client.delete(self.url)
        self.assertEqual(405, response.status_code)
