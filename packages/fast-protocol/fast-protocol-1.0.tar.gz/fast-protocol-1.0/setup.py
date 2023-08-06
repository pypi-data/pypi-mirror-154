# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fast_protocol']
setup_kwargs = {
    'name': 'fast-protocol',
    'version': '1.0',
    'description': 'A very simple Python model for declaring a protocol for checking if objects provide the desired functionality.',
    'long_description': '# fast-protocol\nA very simple Python model for declaring a protocol for checking if objects provide the desired functionality.\n\n## Installation\n```shell\npip install fast-protocol\n```\n\n## Usage\nTo create a Fast Protocol just call the `fast_protocol.protocol` function passing it the names of the methods/attributes that the protocol should support.\n```python\nfrom fast_protocol import protocol\n\ndef example():\n    ...\n\nCallable = protocol("__call__")  # Create a protocol that matches objects with a dunder call method\nmatch example:\n    case Callable():\n        print("example is callable")\n```\nThis can be used outside a `match` statement using `isinstance`.\n```python\nif isinstance(example, Callable):\n    print("example is callable")\n```\n\nProtocols are generated with the name `"FastProtocol"`. This name can be changed by creating a new instance of\n`FastProtocolBuilder`. The name can be set traditionally by passing the name of the protocol to the `FastProtocolBuilder` class. Alternatively you can pass the protocol name as a subscript to an existing `FastProtocolBuilder` which will return a new instance that uses that name.\n\n**Traditional approach:**\n```python\nfrom fast_protocol import FastProtocolBuilder\n\nCallable = FastProtocolBuilder("Callable")("__call__")\n```\n**Alternative approach:**\n```python\nfrom fast_protocol import protocol\n\nCallable = protocol["Callable"]("__call__")\n```\n',
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ZechCodes/fast-protocol',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
