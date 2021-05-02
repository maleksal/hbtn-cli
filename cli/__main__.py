import click

from cli import *

config_manager = ConfigManager()


@click.group()
def main():
    """Create all necessary files of a project. by supplying one or more URL.
    """
    pass


@main.command()
@click.argument('urls', nargs=-1)
@coroutine
async def fetch(urls):
    """Fetch project files and creates them.\n
    Example:

        hbtn fetch https://intranet.hbtn.io/projects/404

        hbtn fetch <URL1> <URL2>
    """
    # read from settings file
    settings = config_manager.read_from_config_settings()
    username, password, location = (settings['username'],
                                    settings['password'],
                                    settings['location'])
    hbtn_instance = Hbtn(username, password)
    file_manager = FileManager(parent_dir=location)
    fetched_projects = await hbtn_instance.start(urls=list(urls))
    for project_data in fetched_projects:
        if project_data:
            await file_manager.process_data(data=project_data)
            click.echo(f"> {project_data['name']} [Done]")


@main.group()
def config():
    """Setup and modify configuration files.

    Examples:

        hbtn config init

        hbtn config show

        hbtn config edit <key> <value>
    """
    pass


# config sub command
@click.command()
@click.option('-username', type=str, prompt="> intranet username")
@click.password_option(confirmation_prompt=False)
@click.option('-location', type=str, prompt="> full path (where/to/save/future/projects)?")
@handle_errors
def init(**kwargs):
    """run a configuration setup
    """
    # create a .ini conf file.
    config_manager.create_config_ini_settings(**kwargs)


# config sub command
@click.command()
@click.option('--username', '-u', type=str, help='Your intranet email')
@click.option('--password', '-u', type=str, help='Your intranet password')
@click.option('--location', '-l', type=str, help='Full path where to save projects Ex:home/.../holberton/')
@handle_errors
def edit(**kwargs):
    """edit values for username, password and location
    """
    # update values
    config_manager.update_config_values(**{k: v for k, v in kwargs.items() if v})


@click.command()
@handle_errors
def show():
    """outputs username and location to stdin.
    """
    # output to stdin
    [
        click.echo(
            f'{k} = {v}')
        for k, v in config_manager.read_from_config_settings().items()
        if v != 'password'
    ]


@click.command()
def remove():
    """remove config file"""
    config_manager.delete_config_file()


config.add_command(edit)
config.add_command(init)
config.add_command(show)
config.add_command(remove)

if __name__ == "__main__":
    main()
