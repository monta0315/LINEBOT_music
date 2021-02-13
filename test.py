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

    search_response = youtube.search().list(
        part='snippet',
        q=push_text,
        order="relevance",
        type='video',
    ).execute()

    img_url = search_response["items"][0]["snippet"]['thumbnails']["default"]["url"]

    video_url="https://youtu.be/"+search_response["items"][0]["id"]["videoId"]


    #flex_boxに変換
    payload = {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                    "type": "uri",
                    "label": "Line",
                    "uri": "https://linecorp.com/"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Brown Cafe",
                        "size": "xl",
                        "weight": "bold"
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "icon",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                "size": "sm"
                            },
                            {
                                "type": "icon",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                "size": "sm"
                            },
                            {
                                "type": "icon",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                "size": "sm"
                            },
                            {
                                "type": "icon",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                "size": "sm"
                            },
                            {
                                "type": "icon",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
                                "size": "sm"
                            },
                            {
                                "type": "text",
                                "text": "4.0",
                                "flex": 0,
                                "margin": "md",
                                "size": "sm",
                                "color": "#999999"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "margin": "lg",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Place",
                                        "flex": 1,
                                        "size": "sm",
                                        "color": "#AAAAAA"
                                    },
                                    {
                                        "type": "text",
                                        "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                                        "flex": 5,
                                        "size": "sm",
                                        "color": "#666666",
                                        "wrap": True
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Time",
                                        "flex": 1,
                                        "size": "sm",
                                        "color": "#AAAAAA"
                                    },
                                    {
                                        "type": "text",
                                        "text": "10:00 - 23:00",
                                        "flex": 5,
                                        "size": "sm",
                                        "color": "#666666",
                                        "wrap": True
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "flex": 0,
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "CALL",
                            "uri": "https://linecorp.com"
                        },
                        "height": "sm",
                        "style": "link"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "WEBSITE",
                            "uri": "https://linecorp.com"
                        },
                        "height": "sm",
                        "style": "link"
                    },
                    {
                        "type": "spacer",
                        "size": "sm"
                    }
                ]
            }
        }
    }



    #メッセージ作成
    container_obj = FlexSendMessage.new_from_json_dict(payload)


    #メッセージを送信するフェーズ
    line_bot_api.reply_message(event.reply_token, messages=container_obj)


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0", port=port)
