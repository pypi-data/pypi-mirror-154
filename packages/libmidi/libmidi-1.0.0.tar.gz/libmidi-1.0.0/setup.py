# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libmidi', 'libmidi.types', 'libmidi.types.messages', 'libmidi.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libmidi',
    'version': '1.0.0',
    'description': 'MIDI library',
    'long_description': '# libmidi\n\n[![PyPi version](https://img.shields.io/pypi/v/libmidi)](https://pypi.org/project/libmidi/)\n\nlibmidi is a MIDI library written from scratch with object oriented programming and proper typing in mind, while trying to keep overhead as minimal as possible.\n\nThis is supposed to be a replacement to [Mido](https://pypi.org/project/mido/), which seems dead development-wise and it has a log of bugs.\n\nIt follows the official MIDI 1.0 specifications\n\nRequires Python 3.8 or greater\n\n## Installation\n\n```sh\npip3 install libmidi\n```\n\n## Instructions\n```python\n# Open a file\nfrom libmidi.types import MidiFile\n\nMidiFile.from_file("midi.mid")\n```\n\n## License\n\n```\n#\n# Copyright (C) 2022 Sebastiano Barezzi\n#\n# SPDX-License-Identifier: LGPL-3.0-or-later\n#\n```\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SebaUbuntu/libmidi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
