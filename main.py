from os import remove
from pprint import pprint
from json import load
from json import loads
from requests import get
from sseclient import SSEClient
from yt_dlp import YoutubeDL

def string_to_valid_filename(s):
    # taken from https://stackoverflow.com/a/295152
    return "".join([x if x.isalnum() else "_" for x in s])

def handle_queue_item(item, src_dir):
    video_id = item["url"][item["url"].rfind('=')+1:]
    file_location = f'{src_dir}/data/queue/{string_to_valid_filename(item["info"]["title"])}_{video_id}.mp4'
    # download video
    ydl_ops = {
        'format': 'mp4',
        'outtmpl': {'default': file_location}
    }
    with YoutubeDL(ydl_ops) as ydl:
        ydl.download([item["url"]])

def main():
    env_json = open('env.json', encoding='utf-8')
    env_vars = load(env_json)

    queue = loads(get(f'{env_vars["URL"]}/queue', timeout=5).text)['videos']

    messages = SSEClient(f'{env_vars["URL"]}/api/sse')

    for msg in messages:
        if msg.event == 'queueItemAdded':
            queue_item = loads(msg.data)
            queue.append(queue_item)
            handle_queue_item(queue_item, env_vars["VTDI_SRC_DIR"])
        if msg.event == 'queueItemRemoved':
            queue_index = loads(msg.data)
            item = queue[queue_index]
            video_id = item["url"][item["url"].rfind('=')+1:]
            file_location = f'{env_vars["VTDI_SRC_DIR"]}/data/queue/{string_to_valid_filename(item["info"]["title"])}_{video_id}.mp4'
            remove(file_location)
            queue.pop(queue_index)

if __name__ == '__main__':
    main()
