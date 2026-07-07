import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import AiAssistantPersonality
from files_sdk import ai_assistant_personality

class AiAssistantPersonalityTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/ai_assistant_personalities/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        ai_assistant_personality = AiAssistantPersonality(params)
        ai_assistant_personality.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/ai_assistant_personalities/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        ai_assistant_personality = AiAssistantPersonality(params)
        ai_assistant_personality.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/ai_assistant_personalities"), "Mock path does not exist")
    def test_list(self):
        resp = ai_assistant_personality.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/ai_assistant_personalities/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        ai_assistant_personality.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ai_assistant_personalities"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "system_prompt" : "foo",
        }
        ai_assistant_personality.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ai_assistant_personalities/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = ai_assistant_personality.create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/ai_assistant_personalities/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        ai_assistant_personality.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/ai_assistant_personalities/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        ai_assistant_personality.delete(id, params)

if __name__ == '__main__':
    unittest.main()