from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,RichMenu,RichMenuSize,RichMenuArea,RichMenuBounds
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

import psycopg2

import random


app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]
DSN=os.environ["DATABASE_URL"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)



@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    #送信されたテキスト
    push_text = event.message.text

    if push_text == "おすすめ":
        push_videos(event)

    else:
        #pushユーザー
        profile_name = line_bot_api.get_profile(event.source.user_id).display_name

        #youtubeAPIから欲しい動画の情報をゲトる
        search_response=youtubeAPI(push_text)


        #pushメッセージに必要な要素を切り出してくる
        title=search_response["items"][0]["snippet"]["title"]

        img_url = search_response["items"][0]["snippet"]["thumbnails"]["high"]["url"]

        video_url="https://youtu.be/"+search_response["items"][0]["id"]["videoId"]

        #データベースに保存
        pushes = (title, img_url, video_url, profile_name)
        insert_table(pushes)

        #flex_boxに変換
        flex_message = FlexSendMessage(
            alt_text=title,
            contents=msg_create(title,img_url,video_url,profile_name))

        #メッセージを送信するフェーズ
        line_bot_api.reply_message(event.reply_token, flex_message)



#データベースに出力
def insert_table(pushes):
    con = psycopg2.connect(DSN)
    cur = con.cursor()
    query = "INSERT INTO store(title,img_url,video_url,name) VALUES(%s,%s,%s,%s)"
    cur.execute(query, pushes)
    cur.close()
    con.commit()
    con.close()

def push_videos(event):
    con = psycopg2.connect(DSN)
    cur = con.cursor()
    #データ数取得
    cur.execute('SELECT COUNT(*) FROM store')
    total = cur.fetchone()

    #ランダムデータをチョイス
    random.seed
    num = random.randrange(1, total[0] + 1)
    cur.execute("SELECT * FROM store where id=%s", str(num))
    result = cur.fetchone()

    #メッセージを加工して送信するフェーズ
    #flex_boxに変換
    flex_message = FlexSendMessage(
        alt_text=result[0],
        contents=msg_create(result[0], result[1], result[2], result[3]))

    #メッセージを送信するフェーズ
    line_bot_api.reply_message(event.reply_token, flex_message)
    cur.close()
    con.close()


def recommend_video():
    con = psycopg2.connect(DSN)
    cur = con.cursor()
    #データベースに登録されているデータの件数を引っ張ってくる
    num=cur.execute("SELECT COUNT(*) from store;")


#YouTubeAPIから引っ張ってくる
def youtubeAPI(push_text):
    search_response = youtube.search().list(
        part="snippet",
        q=push_text,
        order="relevance",
        type="video",
    ).execute()
    return search_response

def msg_create(title,img_url,video_url,profile_name):
    contents = {
        "type": "bubble",
        "direction": "ltr",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "FROM",
                            "color": "#ffffff66",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": "AtNoM",
                            "color": "#ffffff",
                            "size": "xl",
                            "flex": 4,
                            "weight": "bold"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "TO",
                            "color": "#ffffff66",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": profile_name,
                            "color": "#ffffff",
                            "size": "xl",
                            "flex": 4,
                            "weight": "bold"
                        }
                    ]
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#0367D3",
            "spacing": "md",
            "height": "140px",
            "paddingTop": "22px"
        },
        "hero": {
            "type": "image",
            "url": img_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {"type": "uri", "uri": video_url, "label": "label"}
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "sm"
                },
            ]
        }
    }
    return contents

if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0", port=port)
