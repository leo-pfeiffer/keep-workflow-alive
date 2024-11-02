import os
import json
import logging
import requests
from datetime import datetime
from base64 import b64encode
import pprint

logging.basicConfig(level=logging.INFO)

with open('config.json') as f:
    config = json.load(f)

repositories = config.get('repositories')
owner = config.get('owner')
token = os.getenv('PAT_GITHUB')

if not token:
    raise Exception('No GitHub Personal Access Token provided')

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

logging.info(f'Updating files in {owner}\'s repositories')
logging.info(f'Current timestamp: {timestamp}')
logging.info(f'Updating repositories: {pprint.pformat(repositories)}')

for repository in repositories:
    name = repository.get('name')
    file = repository.get('file', '.keep_alive')

    url = f'https://api.github.com/repos/{owner}/{name}/contents/{file}'
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }

    # Check if the file exists
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json().get('sha')
        logging.info(f'{file} exists in {name}')
    else:
        sha = None

    content = b64encode(timestamp.encode()).decode()
    data = {
        'message': f'Update {file} to {timestamp}',
        'content': content,
        'branch': 'main'
    }

    if sha:
        data['sha'] = sha

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        logging.info(f'Successfully updated {file} in {name}')
    else:
        raise Exception(f'Failed update {file} in {name}: {response.json()}')