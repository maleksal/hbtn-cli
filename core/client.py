"""
Hbtn Module
"""
from typing import List, Dict, Union, Any

import requests
from bs4 import BeautifulSoup

JsonType = Dict[str, Union[List[Dict[str, Union[list, Any]]], Any]]


class Hbtn:
    """
    Class that authenticates to the intranet website,
    and fetches json data of a project referenced by URL.
    """

    __loginURL = "https://intranet.hbtn.io/auth/sign_in"
    __headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) "
                               "Chrome/80.0.3987.87 Safari/537.36"}

    def __init__(self, username: str, password: str):
        """
        :param username:    intranet username.
        :param password:    intranet password.
        """
        # Initiate session
        with requests.Session() as session:
            session.headers.update(self.__headers)
            self.__session = session
        assert self.authenticate(
            username,
            password), "Double check your credentials [Authentication Failed]"

    @staticmethod
    def get_token(html_content: str) -> str:
        """
        Returns extracted auth token from html
        """
        soup = BeautifulSoup(html_content, features='lxml')
        return soup.find('input', attrs={'name': 'authenticity_token'})['value']

    @staticmethod
    def preprocess_data(json_data: JsonType) -> JsonType:
        """
        Cleans the retrieved data.
        """
        return {
            "name": json_data["name"],
            'github_repo': json_data['tasks'][0]['github_repo'],
            'github_dir': json_data['tasks'][0]['github_dir'],
            "tasks": [
                {
                    'title': task['title'],
                    'github_file': [
                        file.strip() for file in task['github_file'].split(',')
                        if file.split('.')[-1] not in ['png', 'jpeg', 'icon', 'jpg']
                    ]
                }
                for task in json_data['tasks']]
        }

    def get_login_page(self) -> str:
        """Get login page.
        :return: response.text
        """
        with self.__session.get(self.__loginURL) as res:
            return res.text

    def authenticate(self, username: str, password: str) -> bool:
        """
        Handles authentication with website using username && password.
        """
        login_page = self.get_login_page()
        payload = {
            'authenticity_token': self.get_token(login_page),
            'user[login]': username,
            'user[password]': password,
            'user[remember_me]': '0',
            'commit': 'Log ' + 'in'}

        # login to website
        with self.__session.post(self.__loginURL, data=payload) as res:
            return 'Invalid Email or password.' not in res.text

    def fetch_project_details(self, url: str) -> Union[JsonType, Dict]:
        """Fetch project details referenced by project URL.
        :param url: project URL.
        :return:    json data or empty dict.
        """
        with self.__session.get(url + ".json") as res:
            if res.status_code in range(200, 299):
                data = self.preprocess_data(res.json())
                data['tasks'].append(
                    {  # Add README.md file :)
                        'title': "README.md file",
                        'github_file': ["README.md"]
                    }
                )
                return data
            return {}
