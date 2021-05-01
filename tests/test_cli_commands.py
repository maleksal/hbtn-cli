import os
import pathlib
import unittest

from click.testing import CliRunner

from cli import __main__


class TestCliCommand(unittest.TestCase):

    def setUp(self):
        # some testing inputs
        self.inputs = ["myuser", "mypass", "mylocation"]
        # change filepath for testing
        self.testing_dir = pathlib.Path(__file__).parent.absolute()
        self.test_filename = 'test.ini'
        self.test_file = os.path.join(self.testing_dir, self.test_filename)
        self.runner = CliRunner()
        __main__.config_manager = __main__.ConfigManager(filename=self.test_filename,
                                                         filepath=self.testing_dir)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_config_init(self):
        """Test config init command with settings.ini
        :return:
        """
        result = self.runner.invoke(
            __main__.config, ['init'], input="\n".join(self.inputs))
        assert not result.exception
        assert result.exit_code == 0
        assert os.path.exists(self.test_file)

    def test_config_show_1(self):
        """Test show command when a .ini file is present.
        """
        self.test_config_init()  # create .ini file
        result = self.runner.invoke(__main__.config, ['show'])
        assert not result.exception
        assert result.exit_code == 0
        for txt in self.inputs:
            self.assertIn(txt, result.output)

    def test_config_show_2(self):
        """Test show command when a .ini file is not present.
        """
        # run command
        result = self.runner.invoke(__main__.config, ['show'])

        assert result.exception
        assert result.exit_code == 1
        assert f"{self.test_filename} not found" in result.output

    def test_config_set_1(self):
        """Test edit command with inputs and .ini file is not present
        """
        to_update = {'--username': 'ubdatedusername',
                     '--password': 'updatedpassword',
                     '--location': 'updatedlocation'
                     }
        result = self.runner.invoke(
            __main__.config, ['edit'], input=" ".join(f"{k}={v}"
                                                     for k, v in to_update.items()))
        assert result.exception
        assert result.exit_code == 1
        assert f"{self.test_filename} not found" in result.output

    def test_config_set_2(self):
        """Test edit command with inputs and .ini file is present
        """
        to_update = {'--username': 'ubdatedusername',
                     '--location': 'updatedlocation'
                     }
        self.test_config_init()  # create .ini file
        full_command = ['edit']
        for k, v in to_update.items():
            full_command.append(k)
            full_command.append(v)

        result = self.runner.invoke(__main__.config, full_command)
        assert not result.exception
        assert result.exit_code == 0
        with open(self.test_file) as f:
            results = f.read().split('\n')
        assert all([True if f"{k[2:]} = {v}" in results else False for k, v in to_update.items()])


if __name__ == '__main__':
    unittest.main()
