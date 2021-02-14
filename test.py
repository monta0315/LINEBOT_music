from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from linebot.exceptions import LineBotApiError

from linebot.models import (
    CarouselColumn, CarouselTemplate, FollowEvent,
    LocationMessage, MessageEvent, TemplateSendMessage,
    TextMessage, TextSendMessage, UnfollowEvent, URITemplateAction, FlexSendMessage
)
import json

import os

from apiclient.discovery import build

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

YOUTUBE_API_KEY = "AIzaSyDWbuxE3tzF4RMnCjC045fPy5Cp9GYRHXM"

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    #送信されたテキスト
    push_text = event.message.text

    #youtubeAPIから欲しい動画の情報をゲトる
    #search_response=youtube(push_text)


    """ #pushメッセージに必要な要素を切り出してくる
    title=search_response["items"][0]["snippet"]["title"]

    img_url = search_response["items"][0]["snippet"]['thumbnails']["default"]["url"]

    video_url="https://youtu.be/"+search_response["items"][0]["id"]["videoId"] """


    #flex_boxに変換
    flex_message = FlexSendMessage(
        alt_text="hello",
        contents=msg_create())




    #メッセージを送信するフェーズ
    line_bot_api.reply_message(event.reply_token,flex_message)


def youtube(push_text):
    search_response = youtube.search().list(
        part='snippet',
        q=push_text,
        order="relevance",
        type='video',
    ).execute()
    return search_response

def msg_create():
    contents = {
        'type': 'bubble',
        'direction': 'ltr',
        'hero': {
            'type': 'image',
            'url': 'https://i.ytimg.com/vi/MwxgUVrj5m4/default.jpg',
            'size': 'full',
            'aspectRatio': '20:13',
            'aspectMode': 'cover',
            'action': {'type': 'uri', 'uri': 'https://youtu.be/MwxgUVrj5m4', 'label': 'label'}
        }
    }
    return contents

if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0", port=port)
