from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='hbtn-cli',
    version='0.0.1',
    author='Malek Salem',
    author_email='1419@holbertonschool.com',
    license="MIT License",
    description='Automates Holberton School projects creation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/maleksal/hbtn-cli',
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4==4.10.0",
        "Click==7.1",
        "requests",
        "lxml",
    ],
    python_requires='>=3.5',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix"
    ],
    entry_points='''
        [console_scripts]
        hbtn=main:main
    '''
)
