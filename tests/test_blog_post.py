import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import BlogPost
from files_sdk import blog_post

class BlogPostTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/blog_posts"), "Mock path does not exist")
    def test_list(self):
        resp = blog_post.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/blog_posts/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = blog_post.create_export()

if __name__ == '__main__':
    unittest.main()