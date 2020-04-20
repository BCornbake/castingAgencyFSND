import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor, movie_shows


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.headers = {'Authorization': ''}
        self.token_for_casting_assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inp1UkQ3ajFJZGFxWHEtVmd4U3V5dSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTUxZDMyNzgzYzUwMGMwZWM2NjNjNCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODczNDk5MjcsImV4cCI6MTU4NzQzNjMyNywiYXpwIjoiS2g3R2NENXlFbnR0NFBsWTRzazExUDY5MG4zVjJ3cEUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.vnPL-RkM0l8hbILr1CdB1RxPMJac2A9hpcYGdEhuj4Cw6ileRUnwRFmbR8FQVVobOP5dJVY-7buC57SwJkEwHaLAzXVNwHuMAziuqk19wvswjKpQRA26SNSoZ51K0vcdg4NIw0SAI8EHqNjaclXyQ57OdFVxkpqM78Tr9wlILpZCVoX-Ssz5eyq5BtKTXhk5sdXTa5YwO7AMARGLQiVm7b4PyhIP45piXWoVh_gotSJOz8EHnbfi-Ial5JuMzbNo2K1xK1IQUma0qEn0O_VFdVio5OFaWGX0hm_WtiDrNiNPtKH7SnHh_c3bKLvBIcDMZLc0Mm85oOOZvINXc7mP0A"
        self.token_for_casting_director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inp1UkQ3ajFJZGFxWHEtVmd4U3V5dSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTUxZTNhMzQ3ZWIwMGMxNzE4MTdmMiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODczNDk4NTEsImV4cCI6MTU4NzQzNjI1MSwiYXpwIjoiS2g3R2NENXlFbnR0NFBsWTRzazExUDY5MG4zVjJ3cEUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.WTJEJdXn8xKYR-EGcvQrHixrhX61tDAh_CSzHpnVVvi23GdY7V8QTySWAXMbXV9wFL3543R7rHQygSBvVHMbSkmpiix5jss7GIdFZ0JZTRLfsQloPRhwGOD8ok23s0OcdESfEANTZA3as9rkyVmnAmIdHxmYqcjSN59v4i_I9KMGes93v5_ZGompyFI7G258MaClbKE8AztTC0IaK9XI4WMlZO534syD04lwfTvuEkgUNlOd8bXN0aHJbdLdBHxHqaHAxku50MNSk-_JA4kR8Usz_wsWVJbDTqUsRVXuXU4f5r0GcDB5YY-32VOIAr9p-OiNDFJA2jcGA4hZ83V_7Q"
        self.token_for_executive_producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inp1UkQ3ajFJZGFxWHEtVmd4U3V5dSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTUxZWNlMThiZTI0MGMyMjU0NjA1MCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODczNDk3MzAsImV4cCI6MTU4NzQzNjEzMCwiYXpwIjoiS2g3R2NENXlFbnR0NFBsWTRzazExUDY5MG4zVjJ3cEUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.qYeCZXwQ35VEXcfgt9v2KOfp7XA3l_JDdVp3AiEbajson87oR-utWCk1hOEQNNlmKx4R_IevRhAMMb6nolBXIyYXUwmRylR4PJnR24MNNGL3FEr4zcQctkUrLRq4-umOA-2yXCCsj7hOAw0Yw1MZxwVqMhiXCe-evtvxr8OIjZegJgoyX0AW_n56dggQpYDy1EaoD5nRRYX5oAOUUgOVbXSby6HndmsHl4pKimSnp4cV1-0yXCDn4Ng41Kn4DSLwOXEKcARXWLIMQOAF5mTSw9-4rbimmsjmLKI6LhUVzIZHQbxPModjHAlXljGqEyTPBRaiYGy3Esil_60HU2IxmA" 
        self.token_for_public_user = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inp1UkQ3ajFJZGFxWHEtVmd4U3V5dSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTg1MjEzZTkzYzRhMGNmYzBmYWU4OCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODczNDk5OTUsImV4cCI6MTU4NzQzNjM5NSwiYXpwIjoiS2g3R2NENXlFbnR0NFBsWTRzazExUDY5MG4zVjJ3cEUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.EgtOXlAknZ80C214qjhSwjOhx0LIZ7Nju3FaBAECPNnJexKHdG_mpUB3liz6bzVgDzPmk4iUcQx3FChaEWgMYuV-NGXbecYl5cQ1yuQ0ODufY2Tgr4Z9kRta0F_nnFsOAQFk6m6BYHxbVbh6VQnjtsfjt4bMC1xeRSfMltRt6_J2HdXBBYVXfbJl4VO_ehZ84ro2_urzyVsjBU1Xjb8HJaUf2V2iRQS8_3IpygOaHnkbt1MShOb_nUZHN3q3uvp3NMBbd_GTgOMGqsVPfbVPKKk1C_RcQlhCjfCUIdxRjsjw25TGL0K_zX8nHTsIt2YgyyhTrnkuAuaLrDy-4dDhUg"
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        def tearDown(self):
            """Executed after reach test"""
            pass


    # test case for showing the information of the actors 
    def test_show_actors(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_assistant
        res = self.client().get('/actors', headers=headers)
        data = json.loads(res.data)
        actor_query = Actor.query.all()
        self.assertEqual(res.status_code, 200)
        for idx, actor in enumerate(actor_query):
            self.assertEqual(
                data['actors'][idx]['name'],
                actor.name
            )


    # test case for verification failure when showing actors 
    def test_verification_failure_for_show_actors(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_public_user
        res = self.client().get('/actors', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


    # test case for showing the information of the movies 
    def test_show_movies(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_assistant
        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)
        movie_query = Movie.query.all()
        self.assertEqual(res.status_code, 200)
        for idx, movie in enumerate(movie_query):
            self.assertEqual(
                data['movies'][idx]['title'],
                movie.title 
            )


    # test case for verification failure when showing actors 
    def test_verification_failure_for_show_movies(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_public_user
        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


    # test case for posting a new actor 
    def test_post_actor(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_director
        res = self.client().post('/actors', headers=headers, json={
            "id":3,
            "name": "Dwayne Johnson",
            "age": 48,
            "gender": "male"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    # test case for posting a new actor with unprocessable entity
    def test_422_for_post_actor(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_director
        res = self.client().post('/actors', headers=headers, json={
            "actor_name": "Dwayne Johnson",
            "age": 48,
            "gender": "male"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)


    # test case for posting a new actor with unauthorization
    def test_401_for_post_actor(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_assistant
        res = self.client().post('/actors', headers=headers, json={
            "actor_name": "Jackey Chen",
            "age": 66,
            "gender": "male"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


    # test case for posting a new movie 
    def test_post_movie(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_executive_producer
        res = self.client().post('/movies', headers=headers, json={
            "id": 3,
            "title": "Lion King",
            "release_data": "07-12-2019"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    # test case for posting a new actor with unprocessable entity
    def test_422_for_post_movie(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_executive_producer
        res = self.client().post('/movies', headers=headers, json={
            "id": 3,
            "name": "Lion King",
            "release": "07-12-2019"
        })
        self.assertEqual(res.status_code, 422)


    # test case for posting a new movie with unauthoriztion
    def test_401_for_post_movie(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_director
        res = self.client().post('/movies', headers=headers, json={
            "id": 4,
            "name": "Lord of the Rings",
            "release": "07-12-2014"
        })
        self.assertEqual(res.status_code, 401)


    # test case for deleting an actor 
    def test_delete_actor(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_director
        res = self.client().delete('/actors/3', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    # test case for deleting an actor with 404
    def test_404_for_delete_actor(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_director
        res = self.client().delete('/actors/100', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)


    # test case for deleting an actor with unauthorization
    def test_401_for_delete_actor(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_assistant
        res = self.client().delete('/actors/1', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


    # test case for deleting a movie 
    def test_delete_movie(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_executive_producer
        res = self.client().delete('/movies/3', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    # test case for deleting a movie with 404
    def test_404_for_delete_movie(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_executive_producer
        res = self.client().delete('/movies/100', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)


    # test case for deleting a movie with unauthorization
    def test_401_for_delete_movie(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_director
        res = self.client().delete('/movies/1', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


    # test case for updating an existing actor 
    def test_patch_actor(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_director
        res = self.client().patch('/actors/1', headers=headers, json={
            "age": 50
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    # test case for patching an existing actor with unprocessable entity
    def test_422_for_patch_actor(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_director
        res = self.client().patch('/actors/1', headers=headers, json={
            "age": 48,
            "gender": "male",
            "movie": "Speed and passion"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)

    
    # test case for updating an existing actor with unauthorization
    def test_401_for_patch_actor(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_assistant
        res = self.client().patch('/actors/1', headers=headers, json={
            "age": 53,
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


    # test case for updating an existing movie 
    def test_patch_movie(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_executive_producer
        res = self.client().patch('/movies/1', headers=headers, json={
            "release_data": "01-01-2020"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    # test case for patching an existing movie with unprocessable entity
    def test_422_for_patch_movie(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_executive_producer
        res = self.client().patch('/movies/1', headers=headers, json={
            "age": 48,
            "gender": "male",
            "movie": "Speed and passion"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)


    # test case for updating an existing movie with unauthorization
    def test_401_for_patch_movie(self):
        headers = self.headers
        headers["Authorization"] = "Bearer " + self.token_for_casting_assistant
        res = self.client().patch('/movies/1', headers=headers, json={
            "release_data": "01-01-2020"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
