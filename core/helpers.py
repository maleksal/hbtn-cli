import os
import pathlib
from base64 import b64encode, b64decode
from configparser import ConfigParser
from typing import List, Tuple, Dict, Any, Union


def encrypted(data: str) -> str:
    """
    Returns a Decoded base64 string.
    """
    return b64encode(data.encode('ascii')).decode('ascii')


def decrypted(data: str) -> str:
    """
    Returns an Encoded password with base64.
    """

    return b64decode(data.encode('ascii')).decode('ascii')


def create_files(root_dir: str, project_details: Union[Dict[str, List[Dict[str, list]]], dict]):
    """
    Create file in a root_dir.
    """
    github_repo = project_details['github_repo']
    github_dir = project_details['github_dir']

    for task in project_details["tasks"]:
        for file in task['github_file']:
            formatted_file = f"{root_dir}/{github_repo}/{github_dir}/{file}"
            dirs = '/'.join(formatted_file.split('/')[:-1]) + '/' \
                if not formatted_file.endswith('/') else formatted_file
            pathlib.Path(dirs).mkdir(parents=True, exist_ok=True)

            if not formatted_file.endswith('/'):
                with open(formatted_file, 'w') as f:
                    f.write("")


class Settings:
    __SETTINGS_FILE = "settings.ini"

    def __init__(self):
        self.__config = ConfigParser()
        self.file_status = os.path.exists(self.__SETTINGS_FILE)

    @property
    def read_from_file(self) -> Tuple:
        """
        Read from settings.ini
        :returns: Tuple(location, username, password)
        """
        assert self.file_status, f"{self.__SETTINGS_FILE} not found"
        self.__config.read(self.__SETTINGS_FILE)
        # Import settings variables
        return (
            self.__config['settings']['location'],
            self.__config['settings']['username'],
            decrypted(self.__config['settings']['password'])
        )

    def write_to_file(self, **kwargs: Dict[str, Any]):
        """
        Write to settings.ini.
        """

        valid_keys = ['username', 'password', 'location']
        self.__config["settings"] = {
            k: v for k, v in kwargs.items() if k in valid_keys
        }
        with open(self.__SETTINGS_FILE, 'w') as conf:
            self.__config.write(conf)

    def setup(self):
        """
        Create a settings.ini file with user credentials.
        """
        messages = [
            "Please enter you Holberton email: ",
            "Please enter your Holberton password (don't worry passwd will be encrypted): ",
            "Please enter full path where you want to save future projects: "
        ]
        settings_ini_variables = ["username", 'password', 'location']

        settings_ini = {}
        for msg, var in zip(messages, settings_ini_variables):
            user_input = str(input(msg))

            if var == "location":
                while not os.path.exists(user_input):
                    print("[!]: SUPPLIED PATH DOES NOT EXIST.")
                    user_input = str(input(msg))
            settings_ini[var] = encrypted(user_input) if var == "password" else user_input

        self.write_to_file(**settings_ini)
