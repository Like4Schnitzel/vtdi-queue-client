from pprint import pprint
from json import load
from json import loads
from requests import get
from sseclient import SSEClient

def main():
    env_json = open('env.json', encoding='utf-8')
    env_vars = load(env_json)

    queue = loads(get(f'{env_vars["URL"]}/queue', timeout=5).text)['videos']
    pprint(queue)

    messages = SSEClient(f'{env_vars["URL"]}/api/sse')

    for msg in messages:
        if msg.event == 'queueItemAdded':
            queue.append(loads(msg.data))
        if msg.event == 'queueItemRemoved':
            queue.pop(loads(msg.data))
        pprint(queue)

if __name__ == '__main__':
    main()
