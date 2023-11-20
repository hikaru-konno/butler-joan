# LINE botのライブラリ
from linebot import LineBotApi
from linebot.models import TextSendMessage
import s3

# 予定を管理するライブラリ
import schedule
import time
from datetime import datetime as dt
import pytz

# LINE botのトークン
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')

# 予定のリスト（日時と内容）
schedule_lis = [
    ('2023-08-18 09:30:00', '朝会'),
    ('2023-08-18 10:00:00', 'プレゼン'),
    ('2023-08-18 12:00:00', '昼食'),
    ('2023-08-18 13:00:00', 'ミーティング'),
    ('2023-08-18 15:00:00', 'レポート提出'),
    ('2023-08-18 17:00:00', '退勤')
]

from calendar import day_abbr
import datetime

date_str = '20230101'

def splitDate(dateStr):
    dateObj = datetime.datetime.strptime(dateStr,"%Y%m%d%H%M")
    year = str(dateObj.year)
    month = str(dateObj.month)
    day = str(dateObj.day)
    hour = str(dateObj.hour)
    minute = str(dateObj.minute)
    return year,month,day,hour,minute

def checkDate(date): 
  try: 
    newDate=datetime.datetime.strptime(date,"%Y%m%d%H%M") 
    return True 
  except ValueError: 
    return False
  
def add(user_id, a_schedule):
  # 引数を文字列に変換する
  year = a_schedule[0]
  month = a_schedule[1]
  day = a_schedule[2]
  hour = a_schedule[3]
  minute = a_schedule[4]
  content = a_schedule[5]
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
  try:
    schedule_list = s3.load_schedules(user_id)
  except:
    s3.write_schedules(user_id, [])
  schedule_list.append((date_time, content))
  s3.write_schedules(user_id, schedule_list)

# 予定の30秒前に通知する関数
def notify_schedule(user_id, schedule_list):
    # 現在時刻を取得
    utc_now = dt.now(pytz.utc)
    jst_now = utc_now.astimezone(pytz.timezone('Asia/Tokyo'))
    current_time = jst_now.strftime('%Y-%m-%d %H:%M:%S')
    # LINE botにメッセージを送信
    schedule_list = s3.load_schedules(user_id)
    # 予定のリストをループ
    for schedule in schedule_list:
        splited = schedule.split(",")
        schedule_time = splited[0]
        schedule_content = splited[1]
        # 現在時刻と予定時刻の差が30秒以内なら通知
        try:
          print("current time:", current_time)
          print("schedule time:", schedule_time)
          print("content:", schedule_content)
          diff = abs(time.mktime(time.strptime(schedule_time, "%Y-%m-%d %H:%M:%S")) - time.mktime(time.strptime(current_time, "%Y-%m-%d %H:%M:%S")))
          print(diff)
        except:
          print("時間計算に失敗")
          continue
        if abs(time.mktime(time.strptime(schedule_time, "%Y-%m-%d %H:%M:%S")) - time.mktime(time.strptime(current_time, "%Y-%m-%d %H:%M:%S"))) <= 1800:
            # 通知した予定はリストから削除
            schedule_list = remove_schedule(schedule_list, splited)
            s3.write_schedules(user_id, schedule_list)
            print("inside func:", f'{schedule_time}に{schedule_content}があります')
            return f'{schedule_time}に{schedule_content}があります'

def remove_schedule(sche_list, remove_strings):

  # リストのコピーを作成
  new_list = sche_list.copy()

  # リストの各要素に対して
  for item in sche_list:
    # 削除したい文字列のいずれかが含まれているか判定
    if all(string in item for string in remove_strings):
      print(item, "を削除")
      # 含まれている場合は、新しいリストからその要素を削除
      new_list.remove(item)
  return new_list


def set_payload_year():

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
        "text": "予定内容の詳細を教えて頂きたく思います。\n以下の例にしたがって、年、月、日、時間、内容の順番で教えてくださいませ。(例：2024年8月24日12時0分で内容が焼肉の場合、「202408241200焼肉」となります。)",
        "size": "xl",
        "weight": "bold",
        "wrap": True
      },
      {
        "type": "text",
        "text": "左下のキーボードから入力できます。5分経っても表示されない場合は再度試してください。", 
        "wrap": True
      }
    ]
  }
}
  return payload

def set_payload_month():

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
        "text": "次に、月を半角で入力してください。",
        "size": "xl",
        "weight": "bold", "wrap": True
      }
    ]
  }
}
    return payload


def set_payload_day():

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
        "text": "次に、日を半角で入力してください。",
        "size": "xl",
        "weight": "bold", "wrap": True
      }
    ]
  }
}
    return payload

def set_payload_hour():

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
        "text": "次に、時間(hour)を半角で入力してください。",
        "size": "xl",
        "weight": "bold", "wrap": True
      }
    ]
  }
}
    return payload


def set_payload_minutes():

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
        "text": "次に、分を半角で入力してください。",
        "size": "xl",
        "weight": "bold", "wrap": True
      }
    ]
  }
}
    return payload


def set_payload_content():

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
        "text": "最後に、内容を入力してください。",
        "size": "xl",
        "weight": "bold", "wrap": True
      }
    ]
  }
}
    return payload

    
def set_payload_end():

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
        "text": "ご入力ありがとうございました。この予定は、30分前にリマインドさせていただきます。",
        "size": "xl",
        "weight": "bold",
        "wrap": True
      }
    ]
  }
}
    return payload

# {
#   "type": "bubble",
#   "hero": {
#     "type": "image",
#     "url": "https://storage.googleapis.com/ttrinity/_img/product/32/32782/1590872/design_img_f_1590872_s.png",
#     "size": "full",
#     "aspectRatio": "20:13",
#     "aspectMode": "cover",
#     "action": {
#       "type": "uri",
#       "uri": "http://linecorp.com/"
#     }
#   },
#   "body": {
#     "type": "box",
#     "layout": "vertical",
#     "contents": [
#       {
#         "type": "text",
#         "text": "Brown Cafe",
#         "weight": "bold",
#         "size": "xl"
#       },
#       {
#         "type": "box",
#         "layout": "vertical",
#         "margin": "lg",
#         "spacing": "sm",
#         "contents": [
#           {
#             "type": "box",
#             "layout": "baseline",
#             "spacing": "sm",
#             "contents": [
#               {
#                 "type": "text",
#                 "text": "Time",
#                 "color": "#aaaaaa",
#                 "size": "sm",
#                 "flex": 1
#               },
#               {
#                 "type": "text",
#                 "text": "10:00 - 23:00",
#                 "wrap": true,
#                 "color": "#666666",
#                 "size": "sm",
#                 "flex": 5
#               }
#             ]
#           }
#         ]
#       }
#     ]
#   }
# }