# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libmidi_io', 'libmidi_io.types', 'libmidi_io.utils']

package_data = \
{'': ['*']}

install_requires = \
['libmidi>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'libmidi-io',
    'version': '1.0.0',
    'description': 'MIDI I/O utils',
    'long_description': '# libmidi_io\n\n[![PyPi version](https://img.shields.io/pypi/v/libmidi_io)](https://pypi.org/project/libmidi_io/)\n\nMIDI I/O utils.\n\nThis additional libmidi package adds basic MIDI I/O support (like mido.ports does). It provides a base abstract MIDI port class with some utils (input and output support being consolidated into one class). It still lacks a lot of features (TCP/IP remote ports, backends, etc), which will be rewrote from scratch with time.\n\nRequires Python 3.8 or greater\n\n## Installation\n\n```sh\npip3 install libmidi_io\n```\n\n## Instructions\n\nTODO\n\n## License\n\n```\n#\n# Copyright (C) 2022 Sebastiano Barezzi\n#\n# SPDX-License-Identifier: LGPL-3.0-or-later\n#\n```\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-midi/libmidi_io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
