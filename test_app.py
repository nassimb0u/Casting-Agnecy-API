import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class Casting_agency(unittest.TestCase):
    """This class represents the casting_agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', '1717531', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each endpoint for successful operation and for expected errors.
    """
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']),6)
    
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
    
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_question(self):
        res = self.client().delete('/questions/13')
        data = json.loads(res.data)
        deleted = Question.query.get(13)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 13)
        self.assertEqual(deleted, None)
    
    def test_404_delete_non_existing(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        res = self.client().post('/questions', json={
            'question': 'How are you?',
            'answer': 'Fine',
            'difficulty': 1,
            'category': 4
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        question = Question.query.get(data['created'])
        self.assertEqual(question.question, 'How are you?')
        self.assertEqual(question.answer, 'Fine')
        self.assertEqual(question.difficulty, 1)
        self.assertEqual(question.category, 5) # categories index in the db start from 1 

    

    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm':'who'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['searchTerm'], 'who')
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_search_questions_empty(self):
        res = self.client().post('/questions', json={'searchTerm':''})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['searchTerm'], '')
        self.assertEqual(len(data['questions']), min(QUESTIONS_PER_PAGE, len(Question.query.all())))
        self.assertEqual(data['total_questions'], len(Question.query.all()))
    
    def test_search_questions_invalide(self):
        res = self.client().post('/questions', json={'searchTerm':'json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['searchTerm'], 'json')
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
    
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), min(QUESTIONS_PER_PAGE, len(Question.query.filter(Question.category == 1).all())))
        self.assertEqual(data['total_questions'], len(Question.query.filter(Question.category == 1).all()))
        self.assertEqual(data['current_category'], Category.query.get(1).type)

    
    def test_404_questions_by_non_existing_category(self):
        res = self.client().get('/categories/99/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_get_next_question_science(self):
        previous_questoins = [22,20]
        res = self.client().post('/quizzes', json={
            'previous_questions': previous_questoins,
            'quiz_category': {'type':'Science', 'id':'0'}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['category'], 1)
        self.assertFalse(data['question']['id'] in previous_questoins)
    
    def test_422_next_question_science_no_more_questions(self):
        previous_questoins = [22,20,21]
        res = self.client().post('/quizzes', json={
            'previous_questions': previous_questoins,
            'quiz_category': {'type':'Science', 'id':'0'}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()