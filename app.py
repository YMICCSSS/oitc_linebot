#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
當用戶關注Line@後，Line會發一個FollowEvent，
我們接受到之後，取得用戶個資，對用戶綁定自定義菜單，會回傳四個消息給用戶
"""

# In[2]:


"""
啟用伺服器基本樣板
"""

# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)
#
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextSendMessage, TemplateSendMessage, ImageSendMessage, FlexSendMessage, CarouselContainer
)
# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent
)

from linebot.models.template import (
    ButtonsTemplate
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入json處理套件
import json

# 載入基礎設定檔
secretFileContentJson = json.load(open("line_secret_key", 'r', encoding="utf-8"))
server_url = secretFileContentJson.get("server_url")

# 設定Server啟用細節
app = Flask(__name__, static_url_path="/images", static_folder="images/")

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))
print(line_bot_api)
print(handler)


# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
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


# In[3]:


'''
用戶菜單功能介紹
    用戶能透過點擊菜單，進行我方希冀之業務功能。

流程
    準備菜單的圖面設定檔
    讀取安全設定檔上的參數
    將菜單設定檔傳給Line
    對Line上傳菜單照片
    檢視現有的菜單
    將菜單與用戶做綁定
    將菜單與用戶解除綁定
    刪除菜單
'''

# In[4]:


'''
菜單設定檔
    設定圖面大小、按鍵名與功能

'''

menuRawData = """
{
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": true,
  "name": "8_4圖文選單第一版",
  "chatBarText": "查看更多資訊",
  "areas": [
    {
      "bounds": {
        "x": 102,
        "y": 72,
        "width": 1546,
        "height": 1530
      },
      "action": {
        "type": "postback",
        "text": "選擇課程",
        "data": "action1"
      }
    },
    {
      "bounds": {
        "x": 1763,
        "y": 127,
        "width": 538,
        "height": 631
      },
      "action": {
        "type": "postback",
        "text": "大塚最新研討會",
        "data": "action2"
      }
    },
    {
      "bounds": {
        "x": 1746,
        "y": 847,
        "width": 563,
        "height": 640
      },
      "action": {
        "type": "postback",
        "text": "e購網尚在建置中",
        "data": "action3"
      }
    }
  ]
}
"""

# In[5]:


'''
==============================================================
=========== 圖文選單 ==========================================
======= 如果不小心上傳太多重複的圖文選單到Line Bot上， ===========
======= 先查詢這隻Line Bot上總共有多少圖文選單，全部刪掉 =========
==============================================================
'''

# 讓 Line_bot_api 查詢，現有創建的圖文選單
# rich_menu_list = line_bot_api.get_rich_menu_list()
# for rich_menu in rich_menu_list:
#     line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)


# In[6]:


'''
讀取安全檔案內的字串，以供後續程式碼調用
'''
import json

secretFileContentJson = json.load(open("line_secret_key", 'r', encoding="utf-8"))

print(secretFileContentJson.get("channel_access_token"))
print(secretFileContentJson.get("secret_key"))
print(secretFileContentJson.get("self_user_id"))

# In[7]:


'''
用channel_access_token創建line_bot_api，預備用來跟Line進行溝通
'''

from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))


# In[3]:



'''
載入前面的圖文選單設定，
並要求line_bot_api將圖文選單上傳至Line

'''

from linebot.models import RichMenu
import requests

menuJson = json.loads(menuRawData)

lineRichMenuId = line_bot_api.create_rich_menu(rich_menu=RichMenu.new_from_json_dict(menuJson))
print(lineRichMenuId)



'''
將先前準備的菜單照片，以Post消息寄發給Line
    載入照片
    要求line_bot_api，將圖片傳到先前的圖文選單id
'''

uploadImageFile = open("001.jpg", 'rb')
print(uploadImageFile)
setImageResponse =line_bot_api.set_rich_menu_image(lineRichMenuId, 'image/jpeg', uploadImageFile)
print(setImageResponse)


# In[4]:


'''
將選單綁定到特定用戶身上
    取出上面得到的菜單Id及用戶id
    要求line_bot_api告知Line，將用戶與圖文選單做綁定
'''

rich_menu_list = line_bot_api.get_rich_menu_list()
for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)


# In[13]:


'''
製作文字與圖片的教學訊息
'''
# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

# 消息清單
reply_message_list = [
    TextSendMessage(text="感謝您將大塚官方機器人加為好友，快來與我互動吧!"),
    ImageSendMessage(original_content_url='https://imgur.com/DfWczDA.jpg',
                     preview_image_url='https://imgur.com/DfWczDA.jpg'),
]

# In[14]:


'''
撰寫用戶關注時，我們要處理的商業邏輯
1. 取得用戶個資，並存回伺服器
2. 把先前製作好的自定義菜單，與用戶做綁定
3. 回應用戶，歡迎用的文字消息與圖片消息
'''

# 載入Follow事件
from linebot.models.events import (
    FollowEvent
)

# 載入requests套件
import requests


# 告知handler，如果收到FollowEvent，則做下面的方法處理
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
    print(user_profile)

    # 將用戶資訊存在檔案內
    with open("users.txt", "a") as myfile:
        myfile.write(json.dumps(vars(user_profile), sort_keys=True))
        myfile.write('\r\n')

    # 將菜單綁定在用戶身上
    # linkRichMenuId=secretFileContentJson.get("rich_menu_id")
    linkResult = line_bot_api.link_rich_menu_to_user(event.source.user_id, lineRichMenuId)

    # 回覆文字消息與圖片消息
    line_bot_api.reply_message(
        event.reply_token,
        reply_message_list
    )



# In[15]:


def create_sendmessage_array_from_jsonfile(fileName):
    # 開啟檔案，轉成json
    with open(fileName, 'r', encoding='utf8') as f:
        jsonArray = json.load(f)

    returnArray = []

    for jsonObject in jsonArray:

        # 讀取其用來判斷的元件
        message_type = jsonObject.get('type')

        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'location':
            returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'video':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))

            # 回傳
    return returnArray


# In[7]:


'''
利用Line Designer 做出各種回傳訊息的.json檔案
讀取.json檔案，做出不同的SendMessage
將所有做好的SendMessage，放進字典包起來
依照User傳給我不同的文字，給他不同的回覆
'''

           
A_TemplateSendMessage01 = create_sendmessage_array_from_jsonfile('./JsonFiles/001.json')
A_TemplateSendMessage02 = create_sendmessage_array_from_jsonfile('./JsonFiles/002.json')
A_TemplateSendMessage03 = create_sendmessage_array_from_jsonfile('./JsonFiles/003.json')
A_TemplateSendMessage04 = create_sendmessage_array_from_jsonfile('./JsonFiles/004.json')
A_TemplateSendMessage05 = create_sendmessage_array_from_jsonfile('./JsonFiles/005.json')


# In[8]:


'''
將text動作做成一本字典，當用戶發出相應消息時，可從此進行查找動作。
'''
template_message_dict = {
    "製造業課程": A_TemplateSendMessage02,
    "營建業課程": A_TemplateSendMessage03,
    "建築業課程": A_TemplateSendMessage03,
    "影像行銷課程": A_TemplateSendMessage04,
    "管理應用課程": A_TemplateSendMessage05
}


# In[9]:


'''

當用戶發出文字消息時，判斷文字內容是否包含[::text:]，
    若有，則從template_message_dict 內找出相關訊息
    若無，則回傳預設訊息。

'''

# 用戶發出文字消息時， 按條件內容, 回傳文字消息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    if(event.message.text.find('製造業課程')!= -1):
        line_bot_api.reply_message(
        event.reply_token,
        template_message_dict.get(event.message.text))
        
    if(event.message.text.find('營建業課程')!= -1) or (event.message.text.find('建築業課程')!= -1) :
        line_bot_api.reply_message(
        event.reply_token,
        template_message_dict.get(event.message.text))
        
    if(event.message.text.find('影像行銷課程')!= -1) :
        line_bot_api.reply_message(
        event.reply_token,
        template_message_dict.get(event.message.text))
        
    if(event.message.text.find('管理應用課程')!= -1) :
        line_bot_api.reply_message(
        event.reply_token,
        template_message_dict.get(event.message.text))
        
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="可點擊下方圖片瀏覽其他功能，或直接輸入「營建業課程」、「製造業課程」、「影像行銷課程」、「管理應用課程」可直接找到相關課程"))


# In[10]:


import requests
import datetime
from bs4 import BeautifulSoup as b4


# In[11]:


def get_new(event):
    title_1 = []
    url_1 = []
    get = datetime.datetime.now()
    mon_dic={1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
             7:"July",8:"August",9:"September",10:"October",11:"November",
             12:"December"}

    #印出日期
    month = mon_dic.get(get.month,"")
    month_int = get.month
    day = get.day
    get_today = (f"2020-{month_int}-{day} 大塚資訊最新研討會 ")


    get_data = requests.get("https://www.oitc.com.tw/",headers = {})
    get_data = b4(get_data.text,"lxml")

    #class用class_表示的原因是因為class是Python保留字
    result = get_data.find_all('div', class_="item swiper-slide")

    #注意不可寫成.find_all().find(),只能先以find找到單一元素，再用find_all()往下找更細的內容
    #以下三行可以爬到官網中最新活動
    for i in result:
        result2 = i.find_all("a", class_="figure")
        for j in result2:
            title_1.append(j.get("title"))
            url_1.append(j.get("href"))
            
    #將爬取到的資料排版呈現在使用者手機中
    reply_message_list_oitc = [
        TextSendMessage(text=f"{get_today}"),
        TextSendMessage(
            text="1."+title_1[0]+"\n"+"----\n"+"2."+title_1[1]+"\n"+"----\n"+"3."+title_1[2]+"\n"+"----\n"+"4."+title_1[3]+"\n"+"----\n"+"<詳情請參考以下網址>"+"\n"+"https://www.oitc.com.tw/events/%E7%A0%94%E8%A8%8E%E6%9C%83/1")
    ]

    line_bot_api.reply_message(
        event.reply_token,
        reply_message_list_oitc
    )


# In[12]:



#將callback動作變成一個字典
rep = {
    "action1": A_TemplateSendMessage01
}


def rept(event):
    line_bot_api.reply_message(
        event.reply_token,
        rep.get(event.postback.data)
    )


@handler.add(PostbackEvent)
def handle_post_message(event):
    user_profile = line_bot_api.get_profile(event.source.user_id)
    if (event.postback.data.find('action2') != -1):
        get_new(event)

    else:
        rept(event)



# In[ ]:


'''
執行此句，啟動Server，觀察後，按左上方塊，停用Server
'''

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')


import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])




