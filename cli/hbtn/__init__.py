"""
Hbtn Module
"""
import asyncio

import aiohttp
from bs4 import BeautifulSoup

from ..helpers import url_validator


class Hbtn:
    """
    Asynchronous class that authenticates to the intranet website,
    and fetches json data of a project referenced by URL.
    """

    _loginURL = "https://intranet.hbtn.io/auth/sign_in"
    _headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) "
                              "Chrome/80.0.3987.87 Safari/537.36"}

    def __init__(self, username, password):
        """
        :param username:    intranet username.
        :param password:    intranet password.
        """
        self.__username = username
        self.__password = password
        self._session = None

    @staticmethod
    async def get_token(html_content):
        """
        Returns extracted auth token from html
        """
        soup = BeautifulSoup(html_content,
                             features='lxml')
        return soup.find('input', attrs={'name': 'authenticity_token'})['value']

    async def get_login_page(self):
        """Get login page.
        :return: response.text
        """
        async with self._session.get(self._loginURL) as res:
            return await res.text()

    async def authenticate(self, username, password):
        """
        Handles authentication with website using username && password.
        """
        login_page = await self.get_login_page()
        auth_token = await self.get_token(login_page)
        payload = {
            'authenticity_token': auth_token,
            'user[login]': username,
            'user[password]': password,
            'user[remember_me]': '0',
            'commit': 'Log ' + 'in'}
        # login to website
        async with self._session.post(self._loginURL, data=payload) as res:
            return 'Invalid Email or password.' not in await res.text()

    async def fetch_project_details(self, url):
        """Fetch project details referenced by project URL.
        :param url: project URL.
        :return:    json data or empty dict.
        """
        async with self._session.get(url + ".json") as res:
            if res.status in range(200, 299):
                return await res.json()
            return {}

    @url_validator
    async def start(self, urls):
        """
        Runs coroutines, returns list of dict objects.
        """
        async with aiohttp.ClientSession(headers=self._headers) as session:
            self._session = session
            assert await self.authenticate(
                self.__username,
                self.__password), "Double check your credentials [Authentication Failed]"
            return await asyncio.gather(
                *[asyncio.ensure_future(self.fetch_project_details(url)) for url in urls])
