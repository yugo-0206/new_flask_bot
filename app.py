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

from SentencePiece import reply

line_bot_api = LineBotApi(
    '+ntS4oB83SvQPaUsmW9an6xeGJVWbJpehzqYEQgh7umvDce1Kz3cUU4+pCytsaeXzY037bx3Y7s3z8xdWpoGEQco8zGAilRWH1QkdF7Urm8ha2xGio9+wc6169a+MSeEoNz02wCfFIDwa5jqlmwSpgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('90558eda6523aef272a06a48f1b3a01c')

app = Flask(__name__)


@app.route("/")
def say_hello():
    return "Hello"


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # get request body as text
    # body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)
    # print("----1----")
    # print(body)
    # print("----2----")

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="やぁ!"))

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))

    try:
        reply_text = reply()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text))
    except BaseException:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="返信失敗"))


if __name__ == "__main__":
    app.run()
