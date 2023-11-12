from json import load
from json import loads
from sseclient import SSEClient

env_json = open('env.json', encoding='utf-8')
env_vars = load(env_json)

queue = []

messages = SSEClient(f'{env_vars["URL"]}/api/sse')

for msg in messages:
    if msg.event == 'queueItemAdded':
        queue.append(loads(msg.data))
    if msg.event == 'queueItemRemoved':
        queue.pop(loads(msg.data))
    print(queue)
