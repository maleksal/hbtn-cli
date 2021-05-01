import os
import pathlib
import unittest
from shutil import rmtree

from aiounittest import AsyncTestCase

from cli import ConfigManager
from cli import FileManager


class TestConfigManger(unittest.TestCase):

    def setUp(self):
        self.test_filename = 'test.ini'
        self.testing_dir = pathlib.Path(__file__).parent.absolute()
        self.test_file = os.path.join(self.testing_dir, self.test_filename)
        self.config_manager = ConfigManager(filename=self.test_file,
                                            filepath=self.testing_dir)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_creat_config_ini_setting(self):
        """Test creation of .ini file
        """
        test_values = {
            "username": "myusername",
            "password": "mypassword",
            "location": "mylocation"
        }
        self.config_manager.create_config_ini_settings(**test_values)
        assert os.path.exists(self.test_file)


class TestFileManager(AsyncTestCase):

    def setUp(self):
        self.testing_data = {
            "id": 439,
            "name": "0x01. Test Project",
            "track_id": 'null',
            "created_at": "2018-05-07T21:35:49.000Z",
            "updated_at": "2020-12-15T17:52:11.000Z",
            "tasks": [
                {"id": 3422,
                 "title": "project test",
                 "github_repo": "holbertonschool-test-project",
                 "github_dir": "0x01-testing_project",
                 "github_file": "README.md,"
                                "test_module/test_fileA.c,"
                                "test_module/test_fileA.py,"
                                "test_module2/test_fileA.html,"
                                "test_fileA.txt",
                 "position": 13,
                 "checker_available": 'true'
                 }
            ]}
        self.testing_dir = pathlib.Path(__file__).parent.absolute()
        self.file_manager = FileManager(parent_dir=self.testing_dir)

    def tearDown(self):
        self.folder = os.path.join(
            self.testing_dir,
            self.testing_data['tasks'][0]['github_repo'])
        if os.path.exists(self.folder):
            rmtree(self.folder)

    async def test_process_data_method_1(self):
        """Test file creation. when supplying a github dir.
        """
        repo = f"{self.testing_data['tasks'][0]['github_repo']}/{self.testing_data['tasks'][0]['github_dir']}"
        # create files
        await self.file_manager.process_data(data=self.testing_data)
        # check if created
        for file in self.testing_data['tasks'][0]['github_file'].split(','):
            assert os.path.exists(os.path.join(
                self.testing_dir, os.path.join(repo, file.strip()))
            )

    async def test_process_data_method_2(self):
        """Test file creation. when not supplying a github dir.
        """
        self.testing_data['tasks'][0]['github_dir'] = ""
        repo = self.testing_data['tasks'][0]['github_repo']
        # create files
        await self.file_manager.process_data(data=self.testing_data)
        # check if created
        for file in self.testing_data['tasks'][0]['github_file'].split(','):
            assert os.path.exists(os.path.join(
                self.testing_dir, os.path.join(repo, file.strip()))
            )

    if __name__ == '__main__':
        unittest.main()
