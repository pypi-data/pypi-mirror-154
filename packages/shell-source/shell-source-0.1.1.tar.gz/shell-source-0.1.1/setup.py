# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shell_source']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=4.11.4,<5.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'shell-source',
    'version': '0.1.1',
    'description': 'A python module for sourcing variables from shell scripts',
    'long_description': '# python-shell-source\nA python module for sourcing variables from shell scripts.\n\n## Installation\n```sh\n$ pip install shell-source\n```\n\n## Documentation\n\nThe full documentation is available [here](https://abrahammurciano.github.io/python-shell-source/shell_source)\n\n## Usage\nThis module provides a function `source` which attempts to mimic the shell\'s source command.\n\nThe purpose of this function is to allow you to run a shell script which sets either environment variables or local variables, and then give you access to those variables. Normally this is not a straght-forward task, but this function achieves it by running the script in its intended shell then injecting commands to the shell to print its local variables and its environment variables. Finally it collects the shell\'s stdout and parses it to return to you with exactly the data you asked for.\n\n### Basic Usage\n\nIf you just pass a script and an interpreter you\'ll get back all the environment variables and local variables visible to and set by the script.\n\n```py\n>>> from shell_source import source\n>>> variables = source("path/to/script.sh", "bash")\n>>> # It returns a dictionary of local and environment variables known by the script.\n>>> variables\n{"USER": "abraham", "PATH": "/bin:/usr/bin", ..., "foo": "bar"}\n```\n\n### Requesting Specific Variables\n\nIf you specify the argument `variables`, then only those variables you passed will be present as keys in the returned dictionary.\n\n```py\n>>> source("path/to/script.sh", "csh", variables=("foo", "bar", "biz"))\n{"foo": ..., "bar": ..., "biz", ...}\n```\n\n### Ignoring Local Variables\n\nIf you don\'t want to obtain any local variables set by the script, but only want the environment variables, you can pass `ignore_locals=True`.\n\n### Supporting Different Shells\n\nThis module has been tested to work with `bash`, `zsh`, `csh`, `tcsh`, `ksh`, and `fish`. You can use any other shell that\'s somewhat posix compliant and supports the keyword "source", but it it doesn\'t work, you may use the `ShellConfig` class to indicate to `source` how to interact with your shell.\n\nThe class `ShellConfig` contains several string templates which are used to run the necessary commands with the shell. If the shell you want to use doesn\'t support any of the commands set by default in that class, you can pass an instance of `ShellConfig` to `source` to override the default templates.\n\nFor example, imagine you have a strange shell that uses `@foo` instead of `$foo` to get the value of the variable foo, and that redirects the output of a command like this:\n```\n$ redirect \'echo hello\' to /path/to/file\n```\n\nYou would call `source` like this to tell it how to interact with your shell:\n```py\nsource(\n\t"path/to/script.sh",\n\t"myshell",\n\tshell_config=ShellConfig(\n\t\tredirect_stdout="redirect \'{cmd}\' to {file}",\n\t\tget_var="@{var}",\n\t)\n)\n```\n',
    'author': 'Abraham Murciano',
    'author_email': 'abrahammurciano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abrahammurciano/python-shell-source',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
