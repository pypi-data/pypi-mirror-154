# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poeblix', 'poeblix.util']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0b1,<2.0']

entry_points = \
{'poetry.application.plugin': ['poeblix = poeblix.plugins:BlixPlugin']}

setup_kwargs = {
    'name': 'poeblix',
    'version': '0.3.1',
    'description': 'Poetry plugin that adds support for building wheel files using the poetry.lock file, and data_files just like in setup.py',
    'long_description': '# poeblix\nPoetry Plugin that adds various features deemed unfit for the official release, but makes sense to me\n\n# Overview\nThese contain custom poetry plugins that enable functionality not available in the official distribution of poetry.  These include:\n\n1. Using the Lock file to build a wheel file with pinned dependencies\n2. Support for data_files (like with setup.py) such as jupyter extensions or font files\n3. Validating a wheel file is consistent with dependencies specified in pyproject.toml/poetry.lock\n4. Validating a docker container\'s `pip freeze` contains dependencies as specified in pyproject.toml/poetry.lock\n\nThese are not supported in Poetry due to debate in the community: https://github.com/python-poetry/poetry/issues/890, https://github.com/python-poetry/poetry/issues/4013, https://github.com/python-poetry/poetry/issues/2778\n\n\n# How to Use\n\n### Prerequisite\n\nPoetry Plugins are only supported in 1.2.0+ which, at the moment (5/29/22), can only be installed when using the [new poetry installer](https://python-poetry.org/docs/master/#installation), and updating to the preview version via\n\n```commandline\npoetry self update --preview\n```\n\n## Installation\n\nYou can add the plugin via poetry\'s CLI:\n\n```commandline\npoetry plugin add poeblix\n```\n\nOr install directly from source/wheel, then add with the same above command using the path to the built dist\n\nTo update the plugin:\n\n```commandline\n# Update to latest\npoetry plugin add poeblix@latest\n\n# Update to specific version\npoetry plugin add poeblix==<version>\n```\n\n## Usage\n\n1. To build a wheel from your package (default uses poetry.lock to pin dependencies in the wheel):\n\n```commandline\npoetry blixbuild\n\n# To disable using lock file for building wheel\npoetry blixbuild --no-lock\n```\n\n2. Validate a wheel file has consistent dependencies and data_files as specified in pyproject.toml/poetry.lock\n\n```commandline\npoetry blixvalidatewheel <path-to-wheel>\n\n# Disable using lock file for validation\npoetry blixvalidatewheel --no-lock <path-to-wheel>\n```\n\n_Note: this validates consistency in both directions_\n\n3. Validate a docker container contains dependencies in a `pip freeze` as specified in pyproject.toml/poetry.lock\n\n```commandline\npoetry blixvalidatedocker <docker-container-ID>\n\n# Disable using lock file for validation\npoetry blixvalidatedocker --no-lock <docker-container-ID>\n```\n\n_Note: this only validates the docker container contains dependencies in the project, but not the other direction_\n\nHere\'s an example series of commands to start up a temporary docker container using its tag, validate it, then stop the temporary container\n\n```\n# This will output the newly running container id\ndocker run --entrypoint=bash -it -d <docker-image-tag>\n\n# Then validate the running docker container, and stop it when done\npoetry blixvalidatedocker <container-id>\ndocker stop <container-id>\n```\n\n4. Adding data_files to pyproject.toml to mimic data_files in setup.py:\n\n```yaml\n...\n\n[tool.blix.data]\ndata_files = [\n    { destination = "share/data/", from = [ "data_files/test.txt", "data_files/anotherfile" ] },\n    { destination = "share/data/threes", from = [ "data_files/athirdfile" ] }\n]\n\n...\n```\n\ndata_files should be under the `[tool.blix.data]` category and is a list of objects, each containing the `destination` data folder, and a `from` list of files to add to the destination data folder.\n\n_Note: the destination is a relative path that installs data to relative to the [installation prefix](https://docs.python.org/3/distutils/setupscript.html#installing-additional-files)_\n\nExample: https://github.com/spoorn/poeblix/blob/main/test/positive_cases/happy_case_example/pyproject.toml\n\n5. For more help on each command, use the --help argument\n\n```commandline\npoetry blixbuild --help\npoetry blixvalidatewheel --help\npoetry blixvalidatedocker --help\n```\n\n# Development\n\n```bash\n# Make a virtual environment on Python 3.9\n# If using virtualenvwrapper, run `mkvirtualenv -p python3.9 venv`\nvirtualenv -p python3.9 venv\n\n# Or activate existing virtualenv\n# If using virtualenvwrapper, run `workon venv`\nsource venv/bin/activate\n\n# installs the plugin in editable mode for easier testing via `poetry install`\n./devtool bootstrap\n\n# Lint checks\n./devtool lint\n\n# Tests\n./devtool test\n\n# Run all checks and tests\n./devtool all\n```\n\n**plugins.py** : contains our plugin that adds the `poetry blixbuild` command for building our wheel file\n\n**validatewheel.py**: adds a `poetry blixvalidatewheel` command that validates a wheel file contains the Required Dist as specified in pyproject.toml/poetry.lock\n\n**validatedocker.py** : adds a command that validates a docker file contains dependencies as specified in pyproject.toml and poetry.lock.  This does *NOT* validate that they are exactly matching, but rather that all dependencies in pyproject.toml/poetry.lock exist in the docker container on the correct versions.  The docker image may contain more extra dependencies\n',
    'author': 'spoorn',
    'author_email': 'spookump@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/spoorn/poeblix',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
