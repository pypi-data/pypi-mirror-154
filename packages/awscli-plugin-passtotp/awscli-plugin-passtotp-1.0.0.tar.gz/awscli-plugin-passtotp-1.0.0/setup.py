# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awscli_plugin_passtotp']

package_data = \
{'': ['*']}

install_requires = \
['botocore>=1.14.14,<2.0.0']

setup_kwargs = {
    'name': 'awscli-plugin-passtotp',
    'version': '1.0.0',
    'description': '',
    'long_description': "# AWS CLI MFA with pass-otp made easy\n\nThis plugin enables aws-cli to directly talk to [pass](https://www.passwordstore.org/)\nto acquire an OATH-TOTP code using the [pass-otp](https://github.com/tadfisher/pass-otp) extension.\n\n## Installation\n\n`awscli-plugin-passtotp` can be installed from PyPI:\n```sh\n$ pip install awscli-plugin-passtotp\n```\n\nIt's also possible to install it just for your user in case you don't have\npermission to install packages system-wide:\n```sh\n$ pip install --user awscli-plugin-passtotp\n```\n\n### Configure AWS CLI\n\nTo enable the plugin, add this to your `~/.aws/config`:\n```ini\n[plugins]\n# If using aws-cli v2 you must specify the path to where the package was installed.\ncli_legacy_plugin_path = /foo/bar/lib/python3.9/site-packages/\n\npasstotp = awscli_plugin_passtotp\n```\n\nAlso make sure to specify a path to a file in your password-store in the profiles managed by pass:\n```ini\n[profile myprofile]\nrole_arn = arn:aws:iam::...\nmfa_serial = arn:aws:iam::...\nmfa_path = foo/aws/bar\n...\n```\n\n## Usage\n\nJust use the `aws` command with a custom role and the plugin will do the rest:\n\n```sh\n$ aws s3 ls --profile myprofile\n2013-07-11 17:08:50 mybucket\n2013-07-24 14:55:44 mybucket2\n```\n\n---\n\n## Acknowledgements\n* Thanks to [@tommie-lie](https://github.com/woowa-hsw0) for the [inspiration for this plugin](https://github.com/tommie-lie/awscli-plugin-yubikeytotp)\n",
    'author': 'Christian Segundo',
    'author_email': 'christian@segundo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/someone-stole-my-name/awscli-plugin-passtotp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
