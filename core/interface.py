import click

from .client import Hbtn
from .helpers import Settings, create_files

settings = Settings()


@click.group()
def main():
    """Create all necessary files of a project. by supplying one or more URL.
    """
    pass


@main.command()
@click.argument('urls', required=True, nargs=-1)
def fetch(urls):
    """Fetch project files and creates them.\n
    Example:
        hbtn fetch https://intranet.hbtn.io/projects/<project_id>
        hbtn fetch <URL1> <URL2>
    """
    if not settings.file_status:
        exit("Settings.ini not found: run hbtn setup :)")
    location, username, password = settings.read_from_file
    client = Hbtn(username, password)
    for url in urls:
        create_files(location, client.fetch_project_details(url))


@main.command()
def setup():
    """
    Create settings.ini.
    Command: hbtn setup
    """
    settings.setup()


if __name__ == "__main__":
    main()
