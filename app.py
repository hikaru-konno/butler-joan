from linebot import LineBotApi, WebhookHandler
from linebot.models import TemplateSendMessage,CarouselTemplate,CarouselColumn, FollowEvent, MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, RichMenuSwitchAction
import os
import json
import sample_chat as sc
import soudan,weather,tensaku,scheduler,sakushi,rich,generation,shopping
import schedule, time
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, URIAction, MessageAction
import s3
import random

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

LINE_BOT_API = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
LINE_HANDLER = WebhookHandler(LINE_CHANNEL_SECRET)

rich.delete_alias()
try:
    rich.rich_menu(LINE_BOT_API)
except:
    print("menu失敗")
# try:
#     rich.rich_menu(LINE_BOT_API)
# except:
#     print("richmenu失敗")

def handler(event, context):
    try:
        signature = event["headers"]["x-line-signature"]
    except :
        # print("remind")
        # text_message = TextMessage(text="これはテストです")
        # LINE_BOT_API.push_message("U08891769b70d96251749b10f6f1d6d57", messages=[text_message])
        try:
            ID_list = s3.load_IDs()
        except:
            return
        for id in ID_list:
            try:
                schedule = s3.load_schedules(id.replace("\n", ""))
            except:
                print("id:", id, "のスケジュールがありませんでした。")
                continue
            message = scheduler.notify_schedule(id.replace("\n", ""), schedule)
            print("outside func:", message)
            messages = TextSendMessage(text=message)
            try:
                LINE_BOT_API.push_message(id.replace("\n", ""), messages=messages)
            except:
                continue
        return
            
            


        return
    
    body = event["body"]

    LINE_HANDLER.handle(body, signature)

    return {     
    "statusCode": 200,
    "body": json.dumps(
            {
                "message": "hello world of python lambda!",
                "event": json.dumps(event),
                "context": json.dumps(context.function_name),
            }
        ),
        }


#@LINE_HANDLER.add(FollowEvent)

talk_count = 0
new_response = ""
past_messages = []

#今執事がなんのタスクを行っているか
#文字なし : デフォルト(何もしていない)
#remind : リマインド
#schedule : スケジュール
#weather : 天気
#shopping : ショッピング
#advice : アドバイス
#repair : 文章添削
#lyrics：作詞
#generation：問題生成

#友達追加時の処理
@LINE_HANDLER.add(FollowEvent)
def follow_message(line_event):
    user_name = LINE_BOT_API.get_profile(line_event.source.user_id).display_name
    user_id = LINE_BOT_API.get_profile(line_event.source.user_id).user_id
    if line_event.type == "follow":# フォロー時のみメッセージを送信
        
        LINE_BOT_API.reply_message(
            line_event.reply_token,# イベントの応答に用いるトークン
            TextSendMessage(text=user_name+"様、初メェ～まして。\n本日から、ご主人様の専属執事となるジョーンと申します。\nご要望がありましたら、メニューからお選びくださいませ。"))
        s3.save_1line_to_local(user_id, "")
        s3.upload_file(s3.get_conversation_path(user_id))
    
@LINE_HANDLER.add(MessageEvent)
def on_message(line_event):
    reply = line_event.message.text
    user_id = LINE_BOT_API.get_profile(line_event.source.user_id).user_id
    try:
        #スケジュールの案内の遷移に用いる変数
        count = s3.load_cnt(user_id)[0]
    except:
        print("load count失敗")
    
    try:
        event = s3.load_event(user_id)[0]
    except:
        s3.save_1line_to_local(user_id, "none")
        s3.upload_file(s3.get_conversation_path(user_id))
        event = s3.load_event(user_id)[0]

    print("event:", event)

    
    if reply == ":advice:":
        #botを「相談」専用のモード(advice)に変更する
        s3.write_event(user_id, "advice")

        #会話履歴をリセット
        s3.write_past(user_id, [])

        #案内のメッセージを表示
        flex_message = FlexSendMessage(alt_text='this is alt_text', contents=soudan.set_payload())
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        return
    elif reply == ":repair:":
        s3.write_event(user_id, "correction")
        s3.write_past(user_id, [])
        
        flex_message = FlexSendMessage(alt_text='this is alt_text', contents=tensaku.set_payload())
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        return
    elif reply == ":weather:":
        #モードの設定
        s3.write_event(user_id, "weather")
        s3.write_past(user_id, [])

        #案内の表示
        flex_message = FlexSendMessage(alt_text='this is alt_text', contents=weather.set_payload())
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        return
    elif reply == ":create_song:":
        #モードの設定
        s3.write_event(user_id, "lyrics")
        s3.write_past(user_id, [])
        
        #案内の表示
        flex_message = FlexSendMessage(alt_text='this is alt_text', contents=sakushi.set_payload())
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        return
    elif reply == ":remind:":
        #モードの設定
        s3.write_event(user_id, "schedule")
        s3.write_past(user_id, [])

        #案内の表示
        flex_message = FlexSendMessage(alt_text='this is alt_text', contents=scheduler.set_payload_year())
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        s3.write_cnt(user_id, "1")
        s3.write_a_schedule(user_id, [])
        return
    elif reply == ":generate:":
        s3.write_event(user_id, "generation")
        s3.write_past(user_id, [])

        flex_message = FlexSendMessage(alt_text='this is alt_text', contents=generation.set_payload())
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        return
    elif reply == ":shopping:":
        s3.write_event(user_id, "shopping")
        s3.write_past(user_id, [])

        flex_message = FlexSendMessage(alt_text='this is alt_text', contents=shopping.set_payload())
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        return
    
    if reply.find(":all_display:") != -1:
        flex_message = FlexSendMessage(alt_text='this is alt_text', contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://img3.imepic.jp/image/20230823/492510.png?4f4cc730107974fe9f15681d09b56609",
    "size": "full",
    "aspectRatio": "20:20",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": "調べてまいりました。",
        "size": "xl",
        "weight": "bold"
      },
      {
        "type": "text",
        "text": reply.replace(":all_display:\n", ""),
        "wrap": True
      }
    ]
  }
})
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        return




    if event == "schedule":
        if count == "0":
            flex_message = FlexSendMessage(alt_text='this is alt_text', contents=scheduler.set_payload_year())
            LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
            s3.write_cnt(user_id, "1")
            s3.write_a_schedule(user_id, [])
        if count == "1":
            if scheduler.checkDate(reply[:12]):
                flex_message = FlexSendMessage(alt_text='this is alt_text', contents=scheduler.set_payload_end())
                LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
                s3.write_cnt(user_id, "0")

                #user_idの登録
                try:
                    ids = s3.load_IDs()
                except:
                    s3.write_IDs([])
                    ids = s3.load_IDs()
            
                isContain = False
                for id in ids:
                    if id == user_id:
                        isContain = True
                        break
            
                if isContain == False:
                    ids.append(user_id + "\n")
                    s3.write_IDs(ids)

                #連想配列に形式変換
                year, month, day, hour, minute = scheduler.splitDate(reply[:12])
                # 月、日、時、分が一桁の場合は先頭に0を付ける
                if len(month) == 1:
                    month = '0' + month
                if len(day) == 1:
                    day = '0' + day
                if len(hour) == 1:
                    hour = '0' + hour
                if len(minute) == 1:
                    minute = '0' + minute
                # 引数を結合して形式に合わせる
                date_time = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':00'

                a_schedule = date_time + "," + reply[12:] + "\n"

                try:
                    schedules = s3.load_schedules(user_id)
                except:
                    s3.write_schedules(user_id, [])
                    schedules = s3.load_schedules(user_id)
                
                schedules.append(a_schedule)
                s3.write_schedules(user_id, schedules)
                return
            else:
                payload = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://img3.imepic.jp/image/20230825/362120.png?b99af98feda2b6bdfc89850ac967c91e",
    "size": "full",
    "aspectRatio": "20:20",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": "与えられた形式に間違いがあります。",
        "size": "xl",
        "weight": "bold",
        "wrap": True
      },
      {
        "type": "text",
        "text": "申し訳ありませんが、もう一度お試しください。", 
        "wrap": True
      }
    ]
  }
}
                flex_message = FlexSendMessage(alt_text='this is alt_text', contents=payload)
                LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
                return
                



        # if count == "0":
        #     flex_message = FlexSendMessage(alt_text='this is alt_text', contents=scheduler.set_payload_year())
        #     LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        #     s3.write_cnt(user_id, "1")
        #     s3.write_a_schedule(user_id, [])
        # if count == "1":
        #     flex_message = FlexSendMessage(alt_text='this is alt_text', contents=scheduler.set_payload_month())
        #     LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        #     s3.write_cnt(user_id, "2")
        #     a_schedule = s3.load_a_schedule(user_id)
        #     a_schedule.append(reply)
        #     s3.write_a_schedule(user_id, a_schedule)
        # if count == "2":
        #     flex_message = FlexSendMessage(alt_text='this is alt_text', contents=scheduler.set_payload_day())
        #     LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        #     s3.write_cnt(user_id, "3")
        #     a_schedule = s3.load_a_schedule(user_id)
        #     a_schedule.append(reply)
        #     s3.write_a_schedule(user_id, a_schedule)
        # if count == "3":
        #     flex_message = FlexSendMessage(alt_text='this is alt_text', contents=scheduler.set_payload_hour())
        #     LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        #     s3.write_cnt(user_id, "4")
        #     a_schedule = s3.load_a_schedule(user_id)
        #     a_schedule.append(reply)
        #     s3.write_a_schedule(user_id, a_schedule)
        # if count == "4":
        #     flex_message = FlexSendMessage(alt_text='this is alt_text', contents=scheduler.set_payload_minutes())
        #     LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        #     s3.write_cnt(user_id, "6")
        #     a_schedule = s3.load_a_schedule(user_id)
        #     a_schedule.append(reply)
        #     s3.write_a_schedule(user_id, a_schedule)
        # if count == "6":
        #     flex_message = FlexSendMessage(alt_text='this is alt_text', contents=scheduler.set_payload_content())
        #     LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        #     s3.write_cnt(user_id, "7")
        #     a_schedule = s3.load_a_schedule(user_id)
        #     a_schedule.append(reply)
        #     s3.write_a_schedule(user_id, a_schedule)
        # if count == "7":
        #     flex_message = FlexSendMessage(alt_text='this is alt_text', contents=scheduler.set_payload_end())
        #     LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        #     s3.write_cnt(user_id, "0")
        #     a_schedule = s3.load_a_schedule(user_id)
        #     a_schedule.append(reply)
        #     s3.write_a_schedule(user_id, a_schedule)
        #     print("[a_schedule]")
        #     for s in a_schedule:
        #         print(s)
        #     year = a_schedule[0]
        #     month = a_schedule[1]
        #     day = a_schedule[2]
        #     hour = a_schedule[3]
        #     minute = a_schedule[4]
        #     content = a_schedule[5]
        #     # 月、日、時、分が一桁の場合は先頭に0を付ける
        #     if len(month) == 1:
        #         month = '0' + month
        #     if len(day) == 1:
        #         day = '0' + day
        #     if len(hour) == 1:
        #         hour = '0' + hour
        #     if len(minute) == 1:
        #         minute = '0' + minute
        #     # 引数を結合して形式に合わせる
        #     date_time = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':00'
        #     try:
        #         schedule_list = s3.load_schedules(user_id)
        #     except:
        #         s3.write_schedules(user_id, [])
        #     schedule_list.append((date_time, content))
        #     s3.write_schedules(user_id, schedule_list)
        #     #scheduler.add(user_id, a_schedule)
        #     try:
        #         ids = s3.load_IDs()
        #     except:
        #         s3.write_IDs([])
            
        #     isContain = False
        #     for id in ids:
        #         if id == user_id:
        #             isContain = True
        #             break
            
        #     if isContain == False:
        #         ids.append(user_id)
        #         s3.write_IDs(ids)

    elif event == "advice":

        #過去の会話履歴の読み込み
        try:
            past_messages = s3.load_past(user_id)
        except:
            s3.write_past(user_id, [])
            past_messages = s3.load_past(user_id)

        #過去の会話内容を維持しながら、chatGPTの返答を受け取る
        new_response, past_messages = sc.situziGPTv2("以下の相談に簡潔に答えてください。相談：、" + reply, past_messages)

        #chatGPTの返答をUIとともに表示
        flex_message = FlexSendMessage(alt_text='this is alt_text', contents=soudan.set_payload_answer(new_response))
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        s3.write_past(user_id, past_messages)
        return
    elif event == "correction":
        new_response, past_messages = sc.situziGPTv2("以下の文書を添削してください。また、添削した箇所も明示してください。文書：\n" + reply, [])
        flex_message = FlexSendMessage(alt_text='this is alt_text', contents=tensaku.set_payload_answer(new_response))
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        s3.write_past(user_id, past_messages)
        return
    elif event == "weather":
        info = sc.getWeatherInfo(reply)
        flex_message = FlexSendMessage(alt_text='this is alt_text', contents = weather.set_payload_answer2(reply,info))
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        return 
    elif event == "lyrics":
        new_response, past_messages = sc.situziGPTv2("以下のキーワードから作詞してください。キーワードは、\n" + reply, [])
        flex_message = FlexSendMessage(alt_text='this is alt_text', contents = sakushi.set_payload_answer(new_response))
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        return 
    elif event == "generation":

           #過去の会話履歴の読み込み
        try:
            past_messages = s3.load_past(user_id)
        except:
            s3.write_past(user_id, [])
            past_messages = s3.load_past(user_id)

        #過去の会話内容を維持しながら、chatGPTの返答を受け取る
        new_response, past_messages = sc.situziGPTv2("以下の条件、出力形式を満す問題を作成してください。出力形式は、必ず問題と解答のみを出力してください。条件は\n" + reply, past_messages)
        flex_message = FlexSendMessage(alt_text='this is alt_text', contents = generation.set_payload_answer(new_response))
        LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        return 
    elif event == "shopping":
        names = []
        prices = []
        urls = []
        icons = []
        columns_list = []
        gradients = shopping.get_gradients(reply)
        prompt = reply + "の素材は"
        for name in gradients:
            prompt += "・" + name + "\n"
        prompt += "であるということを簡潔に案内してください"
        new_response, past_messages = sc.situziGPTv2(prompt, [])
        print("ショッピング紹介文の長さ：", len(new_response))
        columns_list.append(CarouselColumn(title="調べてまいりました。", text=new_response[:29], thumbnail_image_url="https://img3.imepic.jp/image/20230823/492510.png?4f4cc730107974fe9f15681d09b56609", actions=[MessageAction(label="全文を表示", text = ":all_display:\n" + new_response)]))
        for g in gradients:
            name, price, url, icon = shopping.search_gradients(g)
            names.append(name)
            prices.append(price)
            urls.append(url)
            columns_list.append(CarouselColumn(title=name[:29], text=str(price) + "円", thumbnail_image_url=icon, actions=[URIAction(label="商品のリンクに飛ぶ", uri=url)]))
            time.sleep(1)
            print("-------------------------------")

        #new_response, past_messages = sc.situziGPTv2(prompt, [])
        #flex_message = FlexSendMessage(alt_text='this is alt_text', contents = shopping.set_payload_answer(reply, new_response, names, prices, urls, icons))
        #LINE_BOT_API.reply_message(line_event.reply_token, flex_message)
        LINE_BOT_API.reply_message(line_event.reply_token, TemplateSendMessage(alt_text='会話ログを表示しています', template=CarouselTemplate(columns=columns_list[:8])))
        return 