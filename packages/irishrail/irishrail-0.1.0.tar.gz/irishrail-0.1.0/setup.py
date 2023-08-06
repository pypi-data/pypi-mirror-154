# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['irishrail', 'irishrail.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'httpx>=0.23.0,<0.24.0',
 'rich>=12.4.4,<13.0.0',
 'xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['irishrail = irishrail.cli:cli']}

setup_kwargs = {
    'name': 'irishrail',
    'version': '0.1.0',
    'description': '',
    'long_description': '# 🚂 irishrail 🇮🇪\n\n<img width="776" alt="🚂🇮🇪(2)" src="https://user-images.githubusercontent.com/431892/173185574-6d01354e-7c25-4a9e-8a1b-61d6bc795f9c.png">\n\n🚉 Irish Rail live updates in your terminal\n\n### Install\n```\n$ pip install irishrail\n```\n\n### Commands\n```\n❯ irishrail --help\nUsage: irishrail [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  live      Train station updates\n  stations  List all stations available\n```\n\n### Bonus\nUse live command with `-f` option to update timetable every couple of seconds:\n\n```\n❯ irishrail live -f "grand canal dock" \n\n                  Grand Canal Dock\n              Northbound - Southbound\n╔══════════════════╤════════╤═════════════╤════════╗\n║ Destination      │ Due    │ Destination │ Due    ║\n╟──────────────────┼────────┼─────────────┼────────╢\n║ Howth            │ 16 min │ Greystones  │ 13 min ║\n║ Grand Canal Dock │ 24 min │ Bray        │ 27 min ║\n║ Malahide         │ 32 min │ Hazelhatch  │ 28 min ║\n║ Howth            │ 49 min │ Greystones  │ 47 min ║\n║ Dublin Connolly  │ 62 min │             │        ║\n╚══════════════════╧════════╧═════════════╧════════╝\n       Updated at: 2022-06-09 22:54:54.443851\n                Press CTRL-C to exit\n```\n',
    'author': 'Marco Rougeth',
    'author_email': 'rougeth@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rougeth/irishrail',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
