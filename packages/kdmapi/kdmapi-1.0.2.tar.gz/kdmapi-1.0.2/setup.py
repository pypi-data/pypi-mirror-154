# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kdmapi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kdmapi',
    'version': '1.0.2',
    'description': "KDMAPI (Keppy's Direct MIDI API) wrapper for Python",
    'long_description': '# kdmapi\n\n[![PyPi version](https://img.shields.io/pypi/v/kdmapi)](https://pypi.org/project/kdmapi/)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/1a367d8d58e34eb6a86b860d1513081f)](https://www.codacy.com/gh/python-midi/kdmapi/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=python-midi/kdmapi&amp;utm_campaign=Badge_Grade)\n\n[KDMAPI (Keppy\'s Direct MIDI API)](https://github.com/KeppySoftware/OmniMIDI/blob/master/DeveloperContent/KDMAPI.md) wrapper for Python\n\nkdmapi provides both C bindings for OmniMIDI.dll and a Python-friendly wrapper for them\n\nA [Mido](https://pypi.org/project/mido/) backend is also provided, instructions on how to use it are below\n\nRequires Python 3.8 or greater\n\n## Installation\n\n```sh\npip3 install kdmapi\n```\n\nYou will also need to have [OmniMIDI](https://github.com/KeppySoftware/OmniMIDI) installed\n\n## Instructions\n\n```python\nfrom kdmapi import KDMAPI\n\n# Initialize the device\nKDMAPI.InitializeKDMAPIStream()\n\n# Send a short 32-bit MIDI message data\nKDMAPI.SendDirectData(0x0)\n\n# Close the device\nKDMAPI.TerminateKDMAPIStream()\n```\n\n## Mido backend\n\nYou can use KDMAPI as a [Mido](https://pypi.org/project/mido/) output backend\n\n```python\nimport mido\n\n# Set KDMAPI as MIDO backend\nmido.set_backend("kdmapi.mido_backend")\n\n# Open MIDI file\nmidi_file = mido.MidiFile("your_file.mid")\n\nwith mido.open_output() as out:\n    for msg in midi_file.play():\n        out.send(msg)\n```\n\n## License\n\n```\n#\n# Copyright (C) 2022 Sebastiano Barezzi\n#\n# SPDX-License-Identifier: LGPL-3.0-or-later\n#\n```\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-midi/kdmapi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
