# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ready_set_deploy',
 'ready_set_deploy.gatherers',
 'ready_set_deploy.providers',
 'ready_set_deploy.renderers']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0', 'more-itertools>=8.12.0,<9.0.0', 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['rsd = ready_set_deploy.cli:main']}

setup_kwargs = {
    'name': 'ready-set-deploy',
    'version': '1.0.0',
    'description': 'Ready-set-deploy is a deployment framework designed to be offline-first ',
    'long_description': '# Ready-Set-Deploy!\n\nRSD is a deployment framework designed to work offline-first without a centralized controller.\nRSD is not an execution framework, nor does it specify how desired state is defined.\n\n# Usage\n\n```bash\nrsd gather PROVIDER1.ID > provider1_state.json\nrsd gather PROVIDER2.ID > provider2_state.json\nrsd combine provider1_state.json provider2_state.json > host_state.json\nrsd diff host_state.json role_state.json > plan.json\nrsd commands plan.json\n\n# As individual steps with some shortcuts\nbash -x <(rsd diff <(rsd providers role_state.json | rsd gather-all) role_state.json | rsd commands -)\n# Or all together in a single command\nbash -x <(rsd apply-local role_state.json)\n```\n\n# Design\n\nRSD is split into three basic parts: gathering the state, operations on the theoretical state, and rendering a diff into commands.\nThe main design goal is to minimize computational effort and enabling offline manipulation of the ideal system configuration state.\n',
    'author': 'Steven Karas',
    'author_email': 'steven.karas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
