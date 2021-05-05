import requests
import json

ACCESS_TOKEN = "32797754327977543279775425320fcc36332793279775452389e04a9aeaa9a29fcfab7"

GROUP_ID = -35488145


def get_text(offset: int):
    response_json = requests.get(
        f'https://api.vk.com/method/wall.get?access_token={ACCESS_TOKEN}&v=5.52&owner_id={GROUP_ID}&count=1&offset={offset}').text
    parsed = json.loads(response_json)
    print(parsed)
    return str(parsed['response']['items'][0]['text'])