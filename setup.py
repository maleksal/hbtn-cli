from setuptools import setup, find_packages


def read_requirements():
    """Read from requirements.txt."""
    with open('requirements.txt', 'r') as f:
        return f.read().splitlines()


setup(
    name="hbtn-cli",
    version="1.0.0",
    entry_points={
        'console_scripts': [
            'hbtn = cli.__main__:main',
        ],
    },
    packages=find_packages(),
    python_requires="~=3.6",
    install_requires=read_requirements()

)
