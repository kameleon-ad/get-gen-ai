import unittest

from flask_migrate import upgrade

from app import create_app
from app.models import Content


class TestContentsAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        upgrade()
        self.client = self.app.test_client()
        self.content = Content.create(title="Test_Content", content="This is a test", created_by="Test_User")
        self.new_content = {
            'title': 'New content',
            'content': 'This is a new content',
            'created_by': 'Test_User',
        }

    def tearDown(self):
        self.app_ctxt.pop()
        self.app = None
        self.app_ctxt = None

    def test_retrieve_all_contents(self):
        response = self.client.get('/api/contents/')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_content_by_id(self):
        response = self.client.get(f'/api/contents/{self.content.id}')  # assuming '/contents/<id>' is your registered url
        self.assertEqual(response.status_code, 200)

    def test_create_content(self):
        response = self.client.post('/api/contents/', json=self.new_content)  # assuming '/contents' is your registered url
        self.assertEqual(response.status_code, 401, response.text)

    def test_review_content(self):
        response = self.client.put(f'/api/contents/{self.content.id}', json={"review": "Test_Review"})  # assuming '/contents/<id>' is your registered url
        self.assertEqual(response.status_code, 401, response.text)

    def test_delete_content(self):
        response = self.client.delete(f'/api/contents/{self.content.id}')  # assuming '/contents/<id>' is your registered url
        self.assertEqual(response.status_code, 401, response.text)


if __name__ == "__main__":
    unittest.main()
