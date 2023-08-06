# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libmidi', 'libmidi.types', 'libmidi.types.messages', 'libmidi.utils']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx>=5.0.1,<6.0.0', 'sphinx-rtd-theme>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'libmidi',
    'version': '1.0.1',
    'description': 'MIDI library',
    'long_description': '# libmidi\n\n[![PyPi version](https://img.shields.io/pypi/v/libmidi)](https://pypi.org/project/libmidi/)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/dd2f2a04bd6c4165b3e6ea361df9cfa5)](https://www.codacy.com/gh/SebaUbuntu/libmidi/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SebaUbuntu/libmidi&amp;utm_campaign=Badge_Grade)\n[![Documentation Status](https://readthedocs.org/projects/libmidi/badge/?version=latest)](https://libmidi.readthedocs.io/en/latest/?badge=latest)\n\nlibmidi is a MIDI library written from scratch with object oriented programming and proper typing in mind, while trying to keep overhead as minimal as possible.\n\nThis is supposed to be a replacement to [Mido](https://pypi.org/project/mido/), which seems dead development-wise and it has a log of bugs.\n\nIt follows the official MIDI 1.0 specifications\n\nRequires Python 3.8 or greater\n\n## Installation\n\n```sh\npip3 install libmidi\n```\n\n## Instructions\n```python\n# Open a file\nfrom libmidi.types import MidiFile\n\nMidiFile.from_file("midi.mid")\n```\n\nComplete documentation is at [Read the Docs](https://libmidi.readthedocs.io)\n\n## License\n\n```\n#\n# Copyright (C) 2022 Sebastiano Barezzi\n#\n# SPDX-License-Identifier: LGPL-3.0-or-later\n#\n```\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-midi/libmidi',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
