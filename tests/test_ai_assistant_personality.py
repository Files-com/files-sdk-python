import unittest
from tests.base import TestBase
from files_sdk.models import AiAssistantPersonality
from files_sdk import ai_assistant_personality


class AiAssistantPersonalityTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        ai_assistant_personality = AiAssistantPersonality(params)
        result = ai_assistant_personality.update(params)
        self.assert_returns(AiAssistantPersonality.update, result)
        self.assert_typed(ai_assistant_personality)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        ai_assistant_personality = AiAssistantPersonality(params)
        ai_assistant_personality.delete(params)
        self.assert_typed(ai_assistant_personality)

    # Static Methods
    def test_list(self):
        result = ai_assistant_personality.list()
        self.assert_returns(ai_assistant_personality.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = ai_assistant_personality.find(id, params)
        self.assert_returns(ai_assistant_personality.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "system_prompt": "foo",
        }
        result = ai_assistant_personality.create(params)
        self.assert_returns(ai_assistant_personality.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = ai_assistant_personality.update(id, params)
        self.assert_returns(ai_assistant_personality.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = ai_assistant_personality.delete(id, params)
        self.assert_returns(ai_assistant_personality.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()
