# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exaroton']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'exaroton',
    'version': '0.0.3.post1',
    'description': 'Python API wrapper for exaroton',
    'long_description': '# exaroton\n\nA Python Wrapper for the [exaroton API](https://developers.exaroton.com/)\n\nSimply get an API Token from [your Account](https://exaroton.com/account/) and you\'re good to go.\n\n[![Python: 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/downloads)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-red)](https://gitlab.com/ColinShark/exaroton/-/blob/master/LICENSE)\n<!-- [![Gitmoji: 💻🔥](https://img.shields.io/badge/Gitmoji-%F0%9F%92%BB%F0%9F%94%A5-yellow)](https://github.com/carloscuesta/gitmoji#readme) -->\n\n## Installation\n\nexaroton requires Python 3.7 or newer.\n\n```sh\npython3 -m pip install -U exaroton\n```\n\nA Virtual Environment is recommended to not mess with system installs.\nThis module has minimal requirements (`requests`), but you can never be safe enough.\n\n```sh\npython3 -m venv venv\nsource ./venv/bin/activate\npip install exaroton\n```\n\n## Example Usage\n\nCurrently all methods are (in my opinion) well documented and properly typehinted.\nIf you see something wrong, don\'t hestitate to [create an Issue](https://github.com/ColinShark/exaroton/issues/new).\n\nI may create a full list of all available methods, or even utilize readthedocs.org\n\n```python\n# Import exaroton and set our token\n>>> from exaroton import Exaroton\n>>> exa = Exaroton("API_TOKEN")\n\n# Get information about the authenticated account\n>>> exa.get_account()\n{\n    "_": "Account",\n    "name": "Username",\n    "email": "email@example.org",\n    "verified": true,\n    "credits": 420.69\n}\n\n# Get a list of our servers\n>>> exa.get_servers()\n[\n    {\n        "_": "Server",\n        "id": "7ZxuNK5RX879BFaH",  # Thanks, random.org!\n        ...\n    },\n    {\n        "_": "Server",\n        "id": "Kf48Td5iVlr8Xu24",  # Thanks, random.org!\n        ...\n    }\n]\n\n# Upload logs to https://mclo.gs\n>>> exa.upload_logs("7ZxuNK5RX879BFaH")\n{\n    "_": "Logs",\n    "id": "N5FR4K2",  # Thanks, random.org!\n    "url": "https://mclo.gs/N5FR4K2",\n    "raw": "https://api.mclo.gs/1/raw/N5FR4K2"\n}\n\n# Print logs (this\'ll most likely spam your output lol)\n>>> exa.get_server_logs("7ZxuNK5RX879BFaH")\n\'one extremely long string with lines seperated by the newline escape character \\n\'\n# It\'ll print each line seperately when used with `print()`!\n```\n\nAll you need to make calls to the API is the Authentication Token you can get\nfrom your account page. If you make server-specific calls, you\'ll need that\nservers ID, too.\n\n\n## The boring stuff\n\nLicensed under [MIT](https://github.com/ColinShark/exaroton/blob/master/LICENSE)',
    'author': 'Colin',
    'author_email': 'colin@colinshark.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ColinShark/exaroton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
