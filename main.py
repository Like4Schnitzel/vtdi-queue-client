from json import load
from sseclient import SSEClient

env_json = open('env.json', encoding='utf-8')
env_vars = load(env_json)

messages = SSEClient(f'{env_vars["URL"]}/api/sse')

for msg in messages:
    print(msg)
