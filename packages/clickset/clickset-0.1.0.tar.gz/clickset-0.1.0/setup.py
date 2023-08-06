# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clickset']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'confuse>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'clickset',
    'version': '0.1.0',
    'description': 'In-class settings configurable via both click and confuse libraries\x1b',
    'long_description': '# ClickSet\n\nThis library permits easy creation of command-line and persistent settings\ninside a class utilizing the `click` and `confuse` libraries.\n\n```python\nfrom clickset import Setting\nfrom clickset import ClickParams\nfrom clickset import get_config\nimport confuse\nimport click\n\nclass MyClass:\n    verbose = Setting(\n        # confuse storage path\n        \'general.verbose\',\n\n        # click boolean option\n        option = ClickParams(\n            \'--verbose/--quiet\',\n            help = \'Verbose or Quiet Output\'\n        )\n    )\n\n@click.command\n# Load all options set in classes\n@Setting.options\ndef main(**kw):\n    # Get the default global confuse configuration singleton\n    config = get_config()\n    foo = MyClass()\n    print(f"verbose: {foo.verbose}")\n    assert foo.verbose == kw[\'verbose\']\n    assert foo.verbose == config[\'general\'][\'verbose\'].get()\n\nmain([\'--verbose\'])\n```\n',
    'author': 'David Morris',
    'author_email': 'gypsysoftware@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/selcouth/clickset',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
