import unittest
import json
from django.test import Client

class SimpleTest(unittest.TestCase):

    def test_identical_texts_scored_1(self):        
        self.client = Client()
        response = self.client.post('/similar-recognition', json.dumps({'text1': 'Hello, world!', 'text2': 'Hello, world!'}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["Similarity score:"], 1)

    def test_works_for_russian(self):
        self.client = Client()
        response = self.client.post('/similar-recognition', json.dumps({'text1': 'Здравствуй, мир!', 'text2': 'Здравствуй, мир!'}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["Similarity score:"], 1)

    def test_different_languages_scored_0(self):
        self.client = Client()
        response = self.client.post('/similar-recognition', json.dumps({'text1': 'Hello, world!', 'text2': 'Здравствуй, мир!'}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["Similarity score:"], 0)
