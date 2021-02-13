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
    img_url = search_response["items"][0]["snippet"]['thumbnails']["default"]["url"]

    video_url = "https://youtu.be/" + \
        search_response["items"][0]["id"]["videoId"]


    print(img_url)
    print(video_url)

if __name__ == "__main__":
    hello_world()
