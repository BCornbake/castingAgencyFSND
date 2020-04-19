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
        self.token_for_casting_assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inp1UkQ3ajFJZGFxWHEtVmd4U3V5dSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTUxZDMyNzgzYzUwMGMwZWM2NjNjNCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODcwMzE4NjIsImV4cCI6MTU4NzExODI2MiwiYXpwIjoiS2g3R2NENXlFbnR0NFBsWTRzazExUDY5MG4zVjJ3cEUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.3BdyImzrPsl0xy0XuarGRBBRA4FFGWO47D9VGOvjnzrtTCTGVgl5zqmvY-kWpc475XLH0Di00Izz7WwCVP6jSg4y2Up6ybtHoH6PZkGmgOZ8Eocp5P-eg00G-jhqcpr1MA6n2PTjDwq98O1MgX0fqBxrpDJRHWMIZgC56-AIjALnAXFCBpivYWyY4qUvEaEDx5JkxBUQBvK7-8GiWZnut1ac9o8CctOBa_TMMwQzGxt5qkS2aQts6iq-X92ysM4UjPMWvecXtRb0Rj3xKjUdkF6E6483tqvpBwW8jCV4_GXyiw98QtDXmsP72V7z1Hc4S8cgrFiQpog82KSQ-3_1tA"
        self.token_for_casting_director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inp1UkQ3ajFJZGFxWHEtVmd4U3V5dSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTUxZTNhMzQ3ZWIwMGMxNzE4MTdmMiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODcwODg1NzgsImV4cCI6MTU4NzE3NDk3OCwiYXpwIjoiS2g3R2NENXlFbnR0NFBsWTRzazExUDY5MG4zVjJ3cEUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.a0A90inFmDGRQE1Hvdpc90SlhjOIqeyqjQG0t56Cscs8HMTuQ-ngQf0odIQXjZ3zKcFSvsA3GTSMHO0Y2kQeEHSO1wtAXh-C8YNVKezUfJgjXBYdIpNX1nSJ36kyT9uHTHNg9z1JNObcnidx8Loi-rfukiR8TuDnbt-uIMtIaMWk0ydPaNlWfE80F5OXQMNNfZ_ys4Wf6w5yKGzdlrXGfCB3MilH4L_dKiTX66WutUTL5Q7y2Y0ML5taIsi6LBoULHunfFjaTblQZ8peR5awGOJOLRuUDeHBeHPiYIVijWZh2craUk5WmCwNMR1EzfZQwW4Vf-3crfOyZ4sAs1FfYw"
        self.token_for_executive_producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inp1UkQ3ajFJZGFxWHEtVmd4U3V5dSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTUxZWNlMThiZTI0MGMyMjU0NjA1MCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODcwOTA4NjgsImV4cCI6MTU4NzE3NzI2OCwiYXpwIjoiS2g3R2NENXlFbnR0NFBsWTRzazExUDY5MG4zVjJ3cEUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.rrcya39ZIpbSuwRhI_f-37kasDV320zisq30saVjs5gXSrZVKll4oFvMZdKvs23WMGZ_pqLwnTvffowzXdRxV6OR-WgbwY1zfLwRn8UjxAyO_lrTPBrafhou4nBzJdg-h_IWUHsoWUuVNl3HG1nf_tMwsG3miu-O064AOltUGuvaxz5B3GsnTwvSvqmjmjMlBrBnhxBTU5qHzkSsf2W8qYF3AWswlIzozEabzPqFSNm1f9WhC3YvtFc83eUyynuYHTBRb4JfQDMvghq2d6RDWd6Ya4vVEXn2J7_E7DhXY8oftK6aHCUVv9z-RABoQmz9Ewb-2WfUKUbQkXz9elc2qQ" 
        self.token_for_public_user = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inp1UkQ3ajFJZGFxWHEtVmd4U3V5dSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTg1MjEzZTkzYzRhMGNmYzBmYWU4OCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODcwNDA5ODQsImV4cCI6MTU4NzEyNzM4NCwiYXpwIjoiS2g3R2NENXlFbnR0NFBsWTRzazExUDY5MG4zVjJ3cEUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.XRpaolPPAESVyKWDffPaaraGl9QrycpAxDXTXOQObgOMYDU5CaKwRtbolZ0tHeD-Dkvq5czK9PFHFFZmOt33R3mKaoTW91_VPAYS7Px8Z7IZbPOPw5DWxOhq-aNNCYr91e2J-hSCGD8wh1luWZkweU_WkfZfNJx_biDclQjNEGv2UR3cFACWJkmWbaH8oIJqD66h5wIrzMoRd7UOVhSFN61MWrV_rAdznrXyRs7Tl1Ee2wZ8po2MN_HMYddhRF99OYD-w7RFdm9IyFCXBXJn3VnvGBufD3NlqqvyWhq7W0FVJPaQjLxiozzx04zTug_kwgkVuGD2129ktPkgnNYVSQ"
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
