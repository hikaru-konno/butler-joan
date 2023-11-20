from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, URIAction, MessageAction, RichMenuSwitchAction, RichMenuAlias
import os
from linebot import LineBotApi, WebhookHandler
from linebot.models import FollowEvent, MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import json
import requests

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

def set_rich_menus_alias(rich_menu_id, rich_menus_alias_id, LINE_BOT_API):
    alias = RichMenuAlias(
        rich_menu_alias_id=rich_menus_alias_id,
        rich_menu_id=rich_menu_id
    )
    LINE_BOT_API.create_rich_menu_alias(alias)

# エイリアス一覧を取得する
def get_alias():
    url_items = "https://api.line.me/v2/bot/richmenu/alias/list"
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
    }

    response = json.loads(requests.get(url_items, headers=headers).text)
    return response

# エイリアス一覧を取得してすべて削除する
def delete_alias():
    alias_list = get_alias()
    print(f'alias_list={alias_list["aliases"]}')
    for alias in alias_list["aliases"]:
        url_items = (
            f'https://api.line.me/v2/bot/richmenu/alias/{alias["richMenuAliasId"]}'
        )
        headers = {"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"}
        json.loads(requests.delete(url_items, headers=headers).text)
        print(f'{alias["richMenuAliasId"]}クリア')

def rich_menu(LINE_BOT_API): 
    
    rich_menu_to_create01 = RichMenu( 
    size=RichMenuSize(width=2500, height=1686), 
    selected=False, 
    name="richmenu_a", 
    chat_bar_text="メニューA", 
    areas=[
        #切り替え
         RichMenuArea( 
            bounds=RichMenuBounds(x=1666, y=0, width=833, height=643), 
            action=RichMenuSwitchAction(label='Change-richmenu', rich_menu_alias_id='richmenu-alias-b', data='richmenu-changed-to-b')),

         RichMenuArea( 
            bounds=RichMenuBounds(x=0, y=843, width=833, height=843), 
            action=MessageAction(label='天気', text=':weather:')),

         RichMenuArea( 
            bounds=RichMenuBounds(x=833, y=843, width=833, height=843), 
            action=MessageAction(label='ショッピング', text=':shopping:')),

         # RichMenuArea( 
         #    bounds=RichMenuBounds(x=833, y=300, width=833, height=693), 
         #    action=MessageAction(label='文章添削', text='文章添削')),

         RichMenuArea( 
            bounds=RichMenuBounds(x=1666, y=843, width=833, height=843), 
            action=MessageAction(label='スケジュール', text=':remind:')),

         # RichMenuArea( 
         #    bounds=RichMenuBounds(x=833, y=1143, width=833, height=693), 
         #    action=MessageAction(label='作詞', text='作詞')),
            
         # RichMenuArea( 
         #    bounds=RichMenuBounds(x=1666, y=1143, width=833, height=693), 
         #    action=MessageAction(label='問題生成', text='問題生成'))
    ]
   )

    rich_menu_to_create02 = RichMenu(   
    size=RichMenuSize(width=2500, height=1686), 
    selected=False, 
    name="richmenu_b", 
    chat_bar_text="メニューB", 
    areas=[

         RichMenuArea( 
            bounds=RichMenuBounds(x=0, y=0, width=833, height=843), 
            action=MessageAction(label='相談', text=':advice:')),

         RichMenuArea( 
            bounds=RichMenuBounds(x=833, y=0, width=833, height=843), 
            action=URIAction(label='羊', uri='https://www.starico-14.com/stamp/outline/a909380-0.png')),

        #  RichMenuArea( 
        #     bounds=RichMenuBounds(x=833, y=0, width=833, height=843), 
        #     action=MessageAction(label='文章添削', text='文章添削')),
            
         RichMenuArea( 
            bounds=RichMenuBounds(x=0, y=843, width=833, height=843), 
            action=MessageAction(label='作詞', text=':create_song:')),

         RichMenuArea( 
            bounds=RichMenuBounds(x=833, y=843, width=833, height=843), 
            action=MessageAction(label='問題生成', text=':generate:')),

         RichMenuArea( 
            bounds=RichMenuBounds(x=1666, y=843, width=833, height=843), 
            action=MessageAction(label='文章添削', text=':repair:')),

         RichMenuArea( 
            bounds=RichMenuBounds(x=1666, y=0, width=833, height=643), 
            action=RichMenuSwitchAction(label='Change-richmenu', rich_menu_alias_id='richmenu-alias-a', data='richmenu-changed-to-a'))
       
        ] 
    )

   #  rich_menu_to_create_02 = RichMenu(
   #      size=RichMenuSize(width=2500, height=743),  
   #      selected=False,
   #      name="Nice richmenu",
   #      chat_bar_text="Tap here",
   #      areas=[RichMenuArea(
   #      bounds=RichMenuBounds(x=0, y=0, width=2500, height=743),
   #      action=RichMenuSwitchAction(
   #          label='Change Rich Menu', 
   #          data="richmenu-2Change@dummy", 
   #          rich_menu_alias_id='rich_menu_01'))]
   #  )
    

    # import urllib.request 
    # url = "https://img3.imepic.jp/image/20230822/425230.jpg?32accf2d08f110e3eefaa4e346916479"
    # response = urllib.request.urlopen(url) 
    # data = response.read()

    #リッチメニュー作成してID保存
    rich_menu_id_01 = LINE_BOT_API.create_rich_menu(rich_menu=rich_menu_to_create01)
    rich_menu_id_02 = LINE_BOT_API.create_rich_menu(rich_menu=rich_menu_to_create02)
    
    #画像の設定
    with open('richmenu-01.jpg', 'rb') as f:
        LINE_BOT_API.set_rich_menu_image(rich_menu_id_01, 'image/jpeg', f)
      
    with open('richmenu-02.jpg', 'rb') as f:
        LINE_BOT_API.set_rich_menu_image(rich_menu_id_02, 'image/jpeg', f)

    set_rich_menus_alias(rich_menu_id_01, 'richmenu-alias-a', LINE_BOT_API)
    set_rich_menus_alias(rich_menu_id_02, 'richmenu-alias-b', LINE_BOT_API)


    LINE_BOT_API.set_default_rich_menu(rich_menu_id_01) 


