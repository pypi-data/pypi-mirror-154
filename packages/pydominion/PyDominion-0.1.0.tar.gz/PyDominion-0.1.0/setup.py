# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dominion', 'dominion.cards', 'dominion.cards.expansions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydominion',
    'version': '0.1.0',
    'description': 'Play the infamous medieval deck-building strategy game in Python!',
    'long_description': "# PyDominion\n\nPlay the popular medieval card game in python!\n\n![Dominion Cover Art](http://wiki.dominionstrategy.com/images/thumb/6/61/BaseArt.jpg/1280px-BaseArt.jpg)\n\n## Premise\n\nPyDominion allows you play Dominion in Python.\nYou can play as a Human using input prompts in the terminal or a web version.\nBut more interestingly, you can simulate bots playing Dominion.\nWanted to try out a new strategy but don't have the time to play hundreds of games?\nYou're in luck!\n\n## Installation\n\nInstall PyDominion from PyPI using `pip`.\n\n```bash\n\npip install pydominion\n\n```\n\n## Usage\n",
    'author': 'Nate',
    'author_email': 'minecraftcrusher100@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GrandMoff100/PyDominion',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
