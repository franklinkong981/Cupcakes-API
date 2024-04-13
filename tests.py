"""This file contains unit tests and integration tests for the main SQLAlchemy Flask Cupcakes JSON API in a testing database called cupcake_test."""
from unittest import TestCase
from app import create_app
from models import db, connect_db, Cupcake

# Create another application instance that connects to the testing database (bloggit_test) instead fo the main database (bloggit).
app = create_app("cupcakes_test", testing=True)
connect_db(app)
app.app_context().push()

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image_url": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image_url": "http://test.com/cupcake2.jpg"
}

class CupcakeAPITestCase(TestCase):
    """Tests for routes/views of Cupcake API."""

    def setUp(self):
        """Make starter cupcake data to run tests on."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        """Test the route that returns a list of all current cupcakes in the database."""
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image_url": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        """Test the route that returns the information for a specific cupcake that matches the cupcake id provided."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        """Test the route that adds a new cupcake to the database and returns JSON information about it."""
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            # We delete the cupcake id in the json returned because we don't know what it is, we do know what the other
            # attributes are so we test for equalit on these.
            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image_url": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)
    
    def test_update_cupcake(self):
        """Test the route that updates a specific cupcake with information we pass in the body."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json={
                "flavor": "Strawberry",
                "size": "large",
                "rating": 10
            })
            data = resp.json

            self.assertEqual(resp.status_code, 200)
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']
            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "Strawberry",
                    "size": "large",
                    "rating": 10,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })
            self.assertEqual(Cupcake.query.count(), 1)
    
    def test_delete_cupcake(self):
        """Test the route that deletes a specific cupcake whose id in the database matches the id passed in the URL."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)
            data = resp.json

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {
                "message": "deleted"
            })
            self.assertEqual(Cupcake.query.count(), 0)
