from apiclient.discovery import build
import json
from linebot.models import TextSendMessage, FlexSendMessage
import os

YOUTUBE_API_KEY = "AIzaSyDWbuxE3tzF4RMnCjC045fPy5Cp9GYRHXM"

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

#必要なもの
#動画の画像，動画のタイトル，動画の概要欄の文言，

print(os.environ)

def hello_world():
    msg_list=[]
    search_response = youtube.search().list(
        part='snippet',
        q="ヒステリックナイトガール",
        order="relevance",
        type='video',
    ).execute()

    title = search_response["items"][0]["snippet"]["title"]

    img_url = search_response["items"][0]["snippet"]['thumbnails']["default"]["url"]

    video_url = "https://youtu.be/" + \
        search_response["items"][0]["id"]["videoId"]

    contents = {
        'type': 'bubble',
        'direction': 'ltr',
        'hero': {
            'type': 'image',
            'url': img_url,
            'size': 'full',
            'aspectRatio': '20:13',
            'aspectMode': 'cover',
            'action': {'type': 'uri', 'uri': video_url, 'label': 'label'}
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "lg"
                },
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "YouTube_Link",
                        "uri": video_url,
                    }
                },
                {
                    "type": "spacer",
                    "size": "sm"
                }
            ],
            "flex": 0
        }
    }

    print(contents)

"""    #msg=json.dumps(msg)

    container_obj = FlexSendMessage.new_from_json_dict(msg)
    print(container_obj)
 """

if __name__ == "__main__":
    hello_world()
