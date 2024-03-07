import unittest

from flask_migrate import upgrade

from app import create_app
from app.models import Content


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        upgrade()

    def tearDown(self):
        self.app_ctxt.pop()
        self.app = None
        self.app_ctxt = None

    def test_content_model(self):
        with self.app.app_context():
            content = Content.create(title="Test Title", content="Test Content", created_by="Test User")

            assert content.title == "Test Title"
            assert content.content == "Test Content"
            assert content.created_by == "Test User"

            retrieved_content = Content.query.get(content.id)

            assert retrieved_content.title == "Test Title"
            assert retrieved_content.content == "Test Content"
            assert retrieved_content.created_by == "Test User"


if __name__ == "__main__":
    unittest.main()
