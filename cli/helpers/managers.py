"""
Helper functions for config files
"""
import os
import pathlib
from configparser import ConfigParser

from aioify import aioify

from .decorators import encode_pass, decode_pass


class ConfigManager:

    def __init__(self, filename='settings.ini', filepath=None):

        self.filename = filename
        self.file = os.path.join(
            pathlib.Path(__file__).parent.absolute(), filename)
        if filepath is not None:
            self.file = os.path.join(filepath, filename)

    @encode_pass
    def create_config_ini_settings(self, **kwargs):
        """Creates the .ini config file.
        """
        config = ConfigParser()
        config["Settings"] = {
            k: v for k, v in kwargs.items()
        }
        # write to .ini
        with open(self.file, 'w') as conf:
            config.write(conf)

    def read_from_config_settings(self):
        """Reads from a .ini config file.
        :return:    dict object or raise error.
        """
        assert os.path.exists(self.file), f"{self.filename} not found"
        config = ConfigParser()
        config.read(self.file)
        # decode password
        config["Settings"]["password"] = decode_pass(config["Settings"]["password"])
        return config['Settings']

    @encode_pass
    def update_config_values(self, **kwargs):
        """Updates values in a .ini config file.
        """
        config = self.read_from_config_settings()
        for k, v in kwargs.items():
            config[k] = v if v else ""
        self.create_config_ini_settings(**config)


class FileManager:
    ignored_extensions = ['png', 'jpeg', 'icon', 'jpg']

    def __init__(self, parent_dir, ignore=None):
        self.parent_dir = parent_dir
        self.create_files_and_directory = aioify(obj=self.create_files_and_directory)

        if ignore is not None and type(ignore) == list:
            self.ignored_extensions.extend(ignore)

    async def process_data(self, data):
        """Process and create files
        :param data:    dict object.
        """
        # initialize needed data
        repo = data['tasks'][0]['github_repo']
        directory = data['tasks'][0]['github_dir']
        github_path = repo + f'{"/" + directory if directory else ""}'
        filenames, sub_dirs = [], [github_path]

        for task in data['tasks']:
            for file in task['github_file'].split(','):
                # 2nd for loop: Solve multiple filenames "fileA, fileB"
                pos_sub_dir = f"{github_path}/{'/'.join(file.split('/')[:-1]).strip()}" if '/' in file else None
                if pos_sub_dir and pos_sub_dir not in sub_dirs:
                    sub_dirs.append(pos_sub_dir)
                full_p_filename = f'{github_path}/{file.strip()}'
                if not self.ignored_file_extension(file) and full_p_filename not in filenames:
                    filenames.append(full_p_filename)
        # create files and directory
        await self.create_files_and_directory(sub_dirs, filenames)

    def ignored_file_extension(self, file):
        """Checks for ignored extensions.
        :param file:        filename to be checked.
        :return:            True if file has ignored ext, else False.
        """
        return file.split('.')[-1] in self.ignored_extensions

    def create_files_and_directory(self, sub_dirs, filenames):
        """Creates files and directories in a specific path.
        :param sub_dirs:     a list of dirs ans sub_dirs that needs to be created.
        :param filenames     a list of filenames, formatted as path/file.txt
        :return: None
        """
        for dr in sub_dirs:
            # make directory's
            os.makedirs(os.path.join(self.parent_dir, dr), exist_ok=True)
        for file in filenames:
            # create files
            with open(os.path.join(self.parent_dir, file), 'w'):
                pass
