import os
import json
import logging
import requests
from datetime import date
from base64 import b64encode

with open('config.json') as f:
    config = json.load(f)

repositories = config.get('repositories')
owner = config.get('owner')
token = os.getenv('GITHUB_TOKEN')

current_date = date.today().strftime('%Y-%m-%d')

for repository in repositories:
    name = repository.get('name')
    file = repository.get('file', '.keep_alive')

    url = f'https://api.github.com/repos/{owner}/{name}/contents/{file}'
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }

    content = b64encode(current_date.encode()).decode()
    data = {
        'message': f'Update {file} to {current_date}',
        'content': content,
        'branch': 'main'
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        logging.info(f'Successfully created or updated {file} in {name}')
    else:
        logging.error(f'Failed to create or update {file} in {name}: {response.json()}')
