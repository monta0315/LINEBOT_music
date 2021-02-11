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
    print(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    push_text = event.message.text

    search_response = youtube.search().list(
        part='snippet',
        q=push_text,
        order="viewCount",
        type='video',
    ).execute()
    reply_video=search_response["items"][0]["id"]["videoId"]
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="https://youtu.be/"+reply_video))


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0", port=port)
