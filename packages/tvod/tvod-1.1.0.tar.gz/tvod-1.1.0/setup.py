# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tvod']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0']

entry_points = \
{'console_scripts': ['tvod = tvod:_main']}

setup_kwargs = {
    'name': 'tvod',
    'version': '1.1.0',
    'description': 'A package to retrieve Twitch VOD',
    'long_description': "# Twitch VOD\nTool to retrieve Twitch's VOD from the video ID\n\n## Install\n\n## Use\n1. Execute the tool from a terminal \n```bash\ntvod\n```\n\n2. It will ask the video ID (you can find it in twitch's video page). In this (`https://www.twitch.tv/videos/1234567890`) case the ID is `1234567890`\n\n3. It will ask at which resolution watch\n\n4. It will use your browser to watch it.\n",
    'author': 'Marco Ferrati',
    'author_email': 'marco.ferrati@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/jjocram/twitch-vod',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
