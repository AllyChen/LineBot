from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# 爬PotterMore的資訊
import requests
import bs4

def pottermore():
    # get the resource from PotterMore
    res = requests.get('https://www.pottermore.com/')
    root = bs4.BeautifulSoup(res.text, "html.parser")
    home_items = root.find_all("div", class_='home-item__wrapper')
    content=""
    for item in home_items:
        if(item.a.get('class')==['home-item__link']):
            link = item.a.get('href')
            if('http' not in link):
                title = item.find(class_="home-item__title").string
                link = 'https://www.pottermore.com' + link
                content += '{}\n{}\n'.format(title, link)
    return content

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('BKQuouNkvzafJZr8oAnJxMQy4q2XDKknKnn5hMiRUB1XxnyT6aZ1B999zApLtEfXJYVsADVUX7Se4qiEFwxZ2tXhnqVCrF4Gs+mUnReOg5B8O9o0clXkrFf8H6b1iExeXbeqFFjCBJEkeXxKDtWbVwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('6dc439ed466958533f4351a3da5163e4')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    textReply = False
    ImageReply = False

    if(event.message.text == 'pottermore'):
        message = TextSendMessage(text=pottermore())
        textReply = True

    if('艾莉2號' in event.message.text):
        senderMessage = event.message.text.replace("艾莉2號", "")
        # it is empty
        if not senderMessage:
            message = TextSendMessage(text="幹嘛！")
        else:
            message = TextSendMessage(text="你"+senderMessage)
        textReply = True
    
    if(textReply):
        line_bot_api.reply_message(event.reply_token, message)
    
    if(True):
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url='https://images.ctfassets.net/bxd3o8b291gf/2FIZoqUsLe0sguEsIyuuO2/8be548b18af8cb083e8ffd76f23a93d2/HarryPotter_WB_F2_HarryPotterAndHedwigLookingAtHogwarts_Still_100615_Land.jpg?w=500&h=500&fit=thumb&f=center&q=85', preview_image_url='https://images.ctfassets.net/bxd3o8b291gf/2FIZoqUsLe0sguEsIyuuO2/8be548b18af8cb083e8ffd76f23a93d2/HarryPotter_WB_F2_HarryPotterAndHedwigLookingAtHogwarts_Still_100615_Land.jpg?w=500&h=500&fit=thumb&f=center&q=85'))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
