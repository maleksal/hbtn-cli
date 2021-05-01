"""
Test hbtn client class.
"""

from unittest import mock, main

from aiounittest import AsyncTestCase

from cli import Hbtn


class TestHbtnClass(AsyncTestCase):

    def setUp(self):
        self.test_username = "hello"
        self.test_password = "olleh"
        self.client = Hbtn(username=self.test_username,
                           password=self.test_password)

    def tearDown(self):
        pass

    def test_url_validation_1(self):
        """Test with broken urls.
        """
        broken_urls = ["https://www.google.com"]
        with self.assertRaises(AssertionError) as context:
            self.client.start(urls=broken_urls)
        self.assertEqual(
            "Not a valid URL",
            str(context.exception)
        )

    async def test_url_validation_2(self):
        """Test with valid urls.
        """
        valid_urls = ["https://intranet.hbtn.io/projects/439"]
        self.client.get_token = mock.Mock(return_value="token")
        self.client.authenticate = mock.AsyncMock(return_value=False)
        with self.assertRaises(AssertionError) as context:
            await self.client.start(urls=valid_urls)
        self.assertIn(
            "Authentication Failed",
            str(context.exception)
        )


if __name__ == '__main__':
    main()
