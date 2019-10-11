import unittest

from app import app


class TestCase(unittest.TestCase):

    def test_index(self):
        with app.test_client() as c:
            response = c.get('/index')
            assert response.status_code == 200

    def test_upload(self):
        with app.test_client() as c:
            response = c.get('/upload')
            assert response.status_code == 200

    def test_sign_in(self):
        with app.test_client() as c:
            response = c.get('/sign_in')
            assert response.status_code == 200

    def test_sign_out(self):
        with app.test_client() as c:
            response = c.get('/sign_out')
            assert response.status_code == 200

    def test_history(self):
        with app.test_client() as c:
            response = c.get('/history')
            assert response.status_code == 200

    def test_user_profile(self):
        with app.test_client() as c:
            response = c.get('/user_profile')
            assert response.status_code == 200

    def test_review(self):
        with app.test_client() as c:
            response = c.get('/review')
            assert response.status_code == 200

    def test_search(self):
        with app.test_client() as c:
            response = c.get('/search')
            assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()