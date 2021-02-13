from apiclient.discovery import build
from linebot.models import (
    CarouselColumn, CarouselTemplate, FollowEvent,
    LocationMessage, MessageEvent, TemplateSendMessage,
    TextMessage, TextSendMessage, UnfollowEvent, URITemplateAction
)

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
    for i in range(len(search_response['items'])):
        result_dict = {
            "image": search_response["items"][i]["snippet"]['thumbnails']["default"]["url"],
            "title": search_response["items"][i]["snippet"]["title"],
            "description": search_response["items"][i]["snippet"]['description'],
            "actions": {
                "label": "動画を視聴する",
                "videoURL": "https://youtu.be/"+search_response["items"][i]["id"]["videoId"],
            }
        }
        msg_list.append(result_dict)

    columns = [
        CarouselColumn(
            thumbnail_image_url=column["image"],
            title=column["title"],
            text=column["description"],
            actions=[
                {
                    "type": "message",
                    "label": column["actions"]["label"],
                    "text":column["actions"]["videoURL"]
                }
            ]
        )
        for column in msg_list
    ]
    print(columns)

if __name__ == "__main__":
    hello_world()
