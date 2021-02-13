from apiclient.discovery import build
import json
from linebot.models import TextSendMessage, FlexSendMessage

YOUTUBE_API_KEY = "AIzaSyDWbuxE3tzF4RMnCjC045fPy5Cp9GYRHXM"

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

#必要なもの
#動画の画像，動画のタイトル，動画の概要欄の文言，

def hello_world():
    msg_list=[]
    search_response = youtube.search().list(
        part='snippet',
        q="ヒステリックナイトガール",
        order="relevance",
        type='video',
    ).execute()
    msg = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": search_response["items"][0]["snippet"]['thumbnails']["default"]["url"],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "https://youtu.be/"+search_response["items"][0]["id"]["videoId"]
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "Brown Cafe",
                    "weight": "bold",
                    "size": "xl"
                }
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
                        "uri": "https://youtu.be/"+search_response["items"][0]["id"]["videoId"]
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

    #msg=json.dumps(msg)

    container_obj = FlexSendMessage.new_from_json_dict(msg)
    print(container_obj)


if __name__ == "__main__":
    hello_world()
