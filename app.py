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

class PMInfo:
    pass

# get the resource from PotterMore
def pottermore():
    res = requests.get('https://www.pottermore.com/')
    root = bs4.BeautifulSoup(res.text, "html.parser")
    home_items = root.find_all("div", class_='home-item__wrapper')
    contents = []
    for item in home_items:
        if(item.a.get('class')==['home-item__link']):
            link = item.a.get('href')
            if('http' not in link):
                content = PMInfo()
                content.title = item.find(class_="home-item__title").string
                content.link = 'https://www.pottermore.com' + link
                content.image = item.find('picture').source.get('data-srcset')
                contents.append(content)
    return contents

# conbine the title and link
def pmTitleLinkMessage(contents):
    message = ""
    for content in contents:
        message = message + '{}\n{}\n'.format(content.title, content.link)
    return message

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

    if(event.message.text == 'pottermore'):
        message = TextSendMessage(text= pmTitleLinkMessage(pottermore()))
        line_bot_api.reply_message(event.reply_token, message)

    if(event.message.text == 'pottermoreimage'):
        # messages=[]
        # pmInfos = pottermore()
        # for num in range(5):
        #     messages.append(ImageSendMessage(
        #         original_content_url=pmInfos[num].image,
        #         preview_image_url=pmInfos[num].image)
        #     )
        Url_1 = 'https://images.pottermore.com/bxd3o8b291gf/2FIZoqUsLe0sguEsIyuuO2/8be548b18af8cb083e8ffd76f23a93d2/HarryPotter_WB_F2_HarryPotterAndHedwigLookingAtHogwarts_Still_100615_Land.jpg?w=1980&h=2640&fit=thumb&f=center&q=85'
        #Url_2 = '//images.pottermore.com/bxd3o8b291gf/2FIZoqUsLe0sguEsIyuuO2/8be548b18af8cb083e8ffd76f23a93d2/HarryPotter_WB_F2_HarryPotterAndHedwigLookingAtHogwarts_Still_100615_Land.jpg?w=500&h=500&fit=thumb&f=center&q=85'
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=Url_1, preview_image_url=Url_1))

    if('艾莉2號' in event.message.text):
        senderMessage = event.message.text.replace("艾莉2號", "")
        # it is empty
        if not senderMessage:
            message = TextSendMessage(text="幹嘛！")
        else:
            message = TextSendMessage(text="你"+senderMessage)
        line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
