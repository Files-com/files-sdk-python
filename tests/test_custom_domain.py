import unittest
from tests.base import TestBase
from files_sdk.models import CustomDomain
from files_sdk import custom_domain


class CustomDomainTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        custom_domain = CustomDomain(params)
        result = custom_domain.update(params)
        self.assert_returns(CustomDomain.update, result)
        self.assert_typed(custom_domain)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        custom_domain = CustomDomain(params)
        custom_domain.delete(params)
        self.assert_typed(custom_domain)

    # Static Methods
    def test_list(self):
        result = custom_domain.list()
        self.assert_returns(custom_domain.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = custom_domain.find(id, params)
        self.assert_returns(custom_domain.find, result)
        self.assert_typed(result)

    def test_create_allocate_ip(self):
        id = 12345
        params = {
            "id": 12345,
            "count": 12345,
        }
        result = custom_domain.create_allocate_ip(id, params)
        self.assert_returns(custom_domain.create_allocate_ip, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "domain": "foo",
        }
        result = custom_domain.create(params)
        self.assert_returns(custom_domain.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = custom_domain.update(id, params)
        self.assert_returns(custom_domain.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = custom_domain.delete(id, params)
        self.assert_returns(custom_domain.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()
