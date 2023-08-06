# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['internetarchive_youtube']

package_data = \
{'': ['*']}

install_requires = \
['internetarchive>=3.0.0',
 'loguru>=0.6.0',
 'pymongo[srv]>=4.0.2',
 'python-dotenv>=0.20',
 'requests>=2.27',
 'tqdm>=4.60.0',
 'yt-dlp>=2022.5.18']

entry_points = \
{'console_scripts': ['ia-yt = internetarchive_youtube:cli.main',
                     'ia_yt = internetarchive_youtube:cli.main',
                     'internetarchive-youtube = '
                     'internetarchive_youtub:cli.main',
                     'internetarchive_youtube = '
                     'internetarchive_youtub:cli.main']}

setup_kwargs = {
    'name': 'internetarchive-youtube',
    'version': '0.1.0',
    'description': 'Archives YouTube channels by automatically uploading their videos to archive.org',
    'long_description': '# Internetarchive-YouTube\n\n[![Poetry-build](https://github.com/Alyetama/internetarchive-youtube/actions/workflows/poetry-build.yml/badge.svg)](https://github.com/Alyetama/internetarchive-youtube/actions/workflows/poetry-build.yml) [![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.7-blue.svg)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/) \n\n🚀 GitHub Action and CLI to archive YouTube channels by uploading the channel\'s videos to [archive.org](https://archive.org).\n\n- 🧑\u200d💻 To use this tool as a command line interface (CLI), jump to [CLI: Getting Started](<#cli-getting-started-> "CLI: Getting Started").\n- ⚡️ To use this tool as a GitHub Action, jump to [GitHub Action: Getting Started](<#github-action-getting-started-%EF%B8%8F> "GitHub Action: Getting Started").\n\n\n## CLI: Getting Started 🧑\u200d💻\n\n### Requirements:\n- 🐍 [Python>=3.7](https://www.python.org/downloads/)\n\n### ⬇️ Installation:\n```sh\npip install internetarchive-youtube\n```\n\n### 🗃️ Backend database:\n- [Create a backend database (or JSON bin)](<#%EF%B8%8F-creating-a-backend-database> "Creating a backend database") to track the download/upload overall progress.\n\n- If you picked **option 1 (MongoDB)**, export MongoDB connection string as an environment variable:\n```sh\nexport MONGODB_CONNECTION_STRING=mongodb://username:password@host:port\n```\n\n- If you picked **option 2 (JSON bin)**, export JSONBIN master key as an environment variable:\n```sh\nexport JSONBIN_KEY=xxxxxxxxxxxxxxxxx\n```\n\n### ⌨️ Usage:\n```\nusage: ia-yt [-h] [-p PRIORITIZE] [-s SKIP_LIST] [-f] [-t TIMEOUT] [-n] [-a] [-c CHANNELS_FILE] [-S] [-C]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p PRIORITIZE, --prioritize PRIORITIZE\n                        Comma-separated list of channel names to prioritize when processing videos\n  -s SKIP_LIST, --skip-list SKIP_LIST\n                        Comma-separated list of channel names to skip\n  -f, --force-refresh   Refresh the database after every video (Can slow down the workflow significantly, but is useful when running multiple concurrent\n                        jobs\n  -t TIMEOUT, --timeout TIMEOUT\n                        Kill the job after n hours (default: 5.5)\n  -n, --no-logs         Don\'t print any log messages\n  -a, --add-channel     Add a channel interactively to the list of channels to archive\n  -c CHANNELS_FILE, --channels-file CHANNELS_FILE\n                        Path to the channels list file to use if the environment variable `CHANNELS` is not set (default: ~/.yt_channels.txt)\n  -S, --show-channels   Show the list of channels in the channels file\n  -C, --create-collection\n                        Creates/appends to the backend database from the channels list\n```\n\n---\n\n## GitHub Action: Getting Started ⚡️\n\n1. **[Fork this repository](https://github.com/Alyetama/yt-archive-sync/fork).**\n2. **[Create a backend database (or JSON bin)](<#%EF%B8%8F-creating-a-backend-database> "Creating a backend database").**\n3. **Add your *Archive.org* credentials to the repository\'s *Actions* secrets:**\n  - `ARCHIVE_USER_EMAIL`\n  - `ARCHIVE_PASSWORD`\n\n4. **Add a list of the channels you want to archive to the repository\'s Actions secrets:**\n\nThe `CHANNELS` secret should be formatted like this example:\n\n```\nCHANNEL_NAME: CHANNEL_URL\nFOO: CHANNEL_URL\nFOOBAR: CHANNEL_URL\nSOME_CHANNEL: CHANNEL_URL\n```\n\nDon\'t add any quotes around the name or the URL, and make sure to keep one space between the colon and the URL.\n\n\n5. **Add the database secret(s) to the repository\'s *Actions* secrets:**\n\nIf you picked **option 1 (MongoDB)**, add this additional secret:\n  - `MONGODB_CONNECTION_STRING`\n\nIf you picked **option 2 (JSON bin)**, add this additional secret:\n  - `JSONBIN_KEY`  \n\n\n6. **Run the workflow under `Actions` manually with a `workflow_dispatch`, or wait for it to run automatically.**\n\nThat\'s it!\n\n\n## 🏗️ Creating A Backend Database\n\n- **Option 1:**  MongoDB (recommended).\n  - Self-hosted (see: [Alyetama/quick-MongoDB](https://github.com/Alyetama/quick-MongoDB) or [dockerhub image](https://hub.docker.com/_/mongo)).\n  - Free database on [Atlas](https://www.mongodb.com/database/free).\n- **Option 2:** JSON bin (if you want a quick start).\n  - Sign up to JSONBin [here](https://jsonbin.io/login).\n  - Click on `VIEW MASTER KEY`, then copy the key.\n\n---\n\n## 📝 Notes\n\n- Information about the `MONGODB_CONNECTION_STRING` can be found [here](https://www.mongodb.com/docs/manual/reference/connection-string/).\n- Jobs can run for a maximum of 6 hours, so if you\'re archiving a large channel, the job might die, but it will resume in a new job when it\'s scheduled to run.\n- Instead of raw text, you can pass a file path or a file URL with a list of channels formatted as `CHANNEL_NAME: CHANNEL_URL` or in JSON format `{"CHANNEL_NAME": "CHANNEL_URL"}`.\n',
    'author': 'Mohammad Alyetama',
    'author_email': 'malyetama@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
