# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['please']

package_data = \
{'': ['*']}

install_requires = \
['art>=5.6,<6.0',
 'autopep8>=1.6.0,<2.0.0',
 'ics>=0.7,<0.8',
 'imgrender>=0.0.4,<0.0.5',
 'pyfiglet>=0.8.post1,<0.9',
 'python-jsonstore>=1.3.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.3.0,<13.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['please = please.please:main']}

setup_kwargs = {
    'name': 'please-cli',
    'version': '0.1.1',
    'description': 'A new tab page for your terminal',
    'long_description': '# Please - New Tab Page for your Terminal\n\n<p align="center"><img src="please.gif"></img></center>\n\n# Installation\n\n### Method 1:\n\n1. Make sure you have Python 3 installed on your computer.\n2. Open your terminal and paste the command below:\n\n   ```bash\n   pip install please-cli && echo \'please\' >> ~/.`echo $0`rc\n\n   # If you get an error about \'pip not found\', just replace pip with pip3.\n   ```\n\n3. That\'s it! Check if `please` command works in your terminal.\n\n### Method 2:\n\n1. Go to the releases section.\n2. Download the latest release WHL file.\n3. Open terminal and paste the command below:\n\n   ```bash\n   pip install --user ~/Downloads/please_cli* && echo \'please\' >> ~/.`echo $0`rc\n\n   # If you get an error about \'pip not found\', just replace pip with pip3.\n   ```\n\n   Change the path of the file if you downloaded it elsewhere.\n\n4. That\'s it! Check if `please` command works in your terminal.\n\n###### Having trouble with installation or have any ideas? Please create an issue ticket :)\n\n# Commands\n\n```bash\n# Show time, quotes and tasks\nplease\n\n# Add a task\nplease add "TASK NAME"\n\n# Delete a task\nplease delete <TASK NUMBER>\n\n# Mark task as done\nplease done <TASK NUMBER>\n\n# Mark task as undone\npleae undone <TASK NUMBER>\n\n# Show tasks even if all tasks are markded as done\nplease showtasks\n```\n\n# Local Development\n\n1. To get started, first install poetry:\n\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\n\n2. Clone this project\n3. `cd` to the project directory and run virtual environment:\n\n```bash\npoetry shell\n\n# OR THIS, IF \'poetry shell\' doesn\'t work\n\n. "$(dirname $(poetry run which python))/activate"\n```\n\n4. Install all dependencies:\n\n```bash\npoetry install\n```\n\n- `please` will be available to use as a command in the virtual environment after using `poetry install`.\n\n5. Finally, run the python script with:\n\n```bash\npython please/please.py\n```\n\n6. To build a WHL package:\n\n```bash\npoetry build\n```\n\n- The package will be generated in **dist** folder, you can then use pip to install the WHL file.\n\n# Uninstalling\n\nOpen your terminal and type:\n\n```bash\npip uninstall please-cli\n```\n\nand also edit your **.zshrc** or **.bashrc** file and remove the line that says `please` at the end of the file.\n',
    'author': 'Nayam Amarshe',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NayamAmarshe/please',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
