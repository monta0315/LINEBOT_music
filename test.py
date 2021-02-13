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
    TextMessage, TextSendMessage, UnfollowEvent, URITemplateAction
)

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
    #メッセージ作成する際に使用するカラム
    msg_list = []

    #送信されたテキスト
    push_text = event.message.text

    search_response = youtube.search().list(
        part='snippet',
        q=push_text,
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
            thumbnail_image_url=column["imgae"],
            title=column["title"],
            text=column["description"],
            actions=[
                URITemplateAction(
                    label=column["actions"]["label"],
                    uri=column["actions"]["videoURL"],
                )
            ]
        )
        for column in msg_list
    ]

    #メッセージ作成
    messages = TemplateSendMessage(
        alt_text="Watch Videos !!", template=CarouselTemplate(columns=columns))


    #メッセージを送信するフェーズ
    try:
        line_bot_api.reply_message(event.reply_token, messages=messages)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, messages=str(e))


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0", port=port)
