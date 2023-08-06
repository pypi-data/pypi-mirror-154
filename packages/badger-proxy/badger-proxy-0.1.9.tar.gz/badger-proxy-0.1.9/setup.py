# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['badger_proxy', 'badger_proxy.proxy']

package_data = \
{'': ['*']}

install_requires = \
['click-extra>=2.1.1,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'docker>=5.0.3,<6.0.0',
 'mitmproxy>=8.0.0,<9.0.0',
 'netifaces>=0.11.0,<0.12.0',
 'result>=0.8.0,<0.9.0',
 'setproctitle>=1.2.3,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'watchdog>=2.1.7,<3.0.0',
 'zeroconf>=0.38.6,<0.39.0']

entry_points = \
{'console_scripts': ['badger = badger_proxy.cli:badger']}

setup_kwargs = {
    'name': 'badger-proxy',
    'version': '0.1.9',
    'description': 'mDNS-based reverse proxy for naming services on a local network.',
    'long_description': '# badger\n\nmDNS-based reverse proxy for naming services on a local network.\n\n## Sample config\n\nConfiguration should be placed in `~/.badger/config.toml`, but this can be changed with `--config <path>`. The config can also be given as either `JSON`, `YAML`, `YML`, `INI` or `XML`.\n\n```toml\n[badger]\nlevel="INFO" # Set default logging level to INFO.\nenable_docker=false # Disable Docker support.\n\nmappings = [\n    "service1@10.0.0.3:5000", # Map service1.local -> 10.0.0.3:5000.\n    "service2@10.0.0.50:80",  # Map service2.local -> 10.0.0.50:80.\n    "service3@10.0.0.4:5256"  # Map service3.local -> 10.0.0.4:5256.\n]\n```\n',
    'author': 'Hugo Lundin',
    'author_email': 'hugo@lundin.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hugolundin/badger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
