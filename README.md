# HBTN-CLI

Hbtn is a cli-application created for Holberton school students. Create project files, modules... with one step.

<img src="https://github.com/maleksal/hbtn-cli/blob/main/demo.gif"  style="zoom:150%;" />

## Installation

> Minimum Python version is 3.6

```console
# clone the repo
$ git clone https://github.com/maleksal/hbtn-cli.git

# change the working directory to hbtn-cli
$ cd hbtn-cli

# install
$ python3 -m pip install .

# update: cd to hbtn-cli
$ git pull && python3 -m pip install . -U

# uninstall
$ hbtn config remove && python3 -m pip uninstall hbtn-cli
```

> Error msg:  "Can't uninstall 'hbtn-cli'. No files were found to uninstall."
>
> Fix : hbtn config remove && cd /tmp && python3 -m pip uninstall hbtn-cli

## Usage

```console
# Enter your intranet credentials
$ hbtn config init

# To automate a project
$ hbtn fetch <project URL>

$ hbtn --help
Usage: hbtn [OPTIONS] COMMAND [ARGS]...

  Create all necessary files of a project. by supplying one or more URL.

Options:
  --help  Show this message and exit.

Commands:
  config  Setup and modify configuration files.
  fetch   Fetch project files and creates them.

```

