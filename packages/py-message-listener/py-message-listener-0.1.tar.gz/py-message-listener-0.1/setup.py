# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['listener']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.7,<2.0.0']

setup_kwargs = {
    'name': 'py-message-listener',
    'version': '0.1',
    'description': 'sqs message listener using boto3',
    'long_description': "# message-listener\n\nThis module can be used for listening to the messages from aws sqs.\n\n### Requirements\n\n1. install module `pip install py-message-listener`\n\nFollow bellow steps for using this module\n\n1. Add `@Listener` decorator to method or function where do you want to recieve the message, for that method/function\n   add single parameter, This parameter is set whenever the message is recieved and method will be called and message\n   will be passed as argument.\n2. In decorator pass queue name in `destination`   argument\n3. set these environment variables: `AWS_REGION`, `AWS_ACCOUNT_ID`, `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`\n\n> `AWS_ACCOUNT_ID` this will be used for generating the queue url\n\n#### Sample Code\n\n```python\nfrom listener import Listener\n\n\n@Listener(destination='test.fifo')\ndef fun(msg: str):\n    print(msg)\n```\n",
    'author': 'Raju Komati',
    'author_email': 'komatiraju032@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
