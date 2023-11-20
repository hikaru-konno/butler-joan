#s3にファイルをアップロードする関数
def upload_file(file):
    import boto3
    s3 = boto3.resource('s3') 
    bucket = s3.Bucket("2023-intern-s3-team2") 
    bucket.upload_file(file, file)

#s3からファイルをダウンロードする関数
def download_file(file):
    import boto3
    s3 = boto3.resource('s3') 
    bucket = s3.Bucket("2023-intern-s3-team2") 
    bucket.download_file(file, file)


#現在のイベントを読み込み
def load_event(user_id):
    download_file(get_conversation_path(user_id))
    event = load_lines(user_id)
    return event

#過去のメッセージを読み込み
def load_past(user_id):
    download_file(get_conversation_path(user_id + "past_message"))
    past = load_lines(user_id + "past_message")
    return past

def load_cnt(user_id):
    download_file(get_conversation_path(user_id + "_cnt"))
    past = load_lines(user_id + "_cnt")
    return past

def load_a_schedule(user_id):
    download_file(get_conversation_path(user_id + "_a_schedule"))
    past = load_lines(user_id + "_a_schedule")
    return past

def load_schedules(user_id):
    download_file(get_conversation_path(user_id + "_schedules"))
    past = load_lines(user_id + "_schedules")
    return past

def load_IDs():
    download_file(get_conversation_path("IDs"))
    past = load_lines("IDs")
    return past

def write_event(user_id, event):
    save_1line_to_local(user_id, event)
    upload_file(get_conversation_path(user_id))

def write_past(user_id, mes):
    save_lines_to_local(user_id + "past_message", mes)
    upload_file(get_conversation_path(user_id + "past_message"))

def write_cnt(user_id, cnt):
    save_1line_to_local(user_id + "_cnt", cnt)
    upload_file(get_conversation_path(user_id + "_cnt"))

def write_a_schedule(user_id, content):
    save_lines_to_local2(user_id + "_a_schedule", content)
    upload_file(get_conversation_path(user_id + "_a_schedule"))

def write_schedules(user_id, content):
    save_lines_to_local2(user_id + "_schedules", content)
    upload_file(get_conversation_path(user_id + "_schedules"))

def write_IDs(content):
    save_lines_to_local2("IDs", content)
    upload_file(get_conversation_path("IDs"))

#ユーザーごとの会話ファイルパスを生成する関数
def get_conversation_path(user_id):
    conversation_folder = '/tmp/'
    return conversation_folder + user_id + '.txt'

#文字列をファイルに書き込む
def save_1line_to_local(user_id, content):
    file_path = get_conversation_path(user_id)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

#リストをファイルに書き込む
def save_lines_to_local(user_id, content):
    file_path = get_conversation_path(user_id)
    with open(file_path, "w", encoding="utf-8") as file:
        for c in content:
            print(c) 
            file.writelines(c)

def save_lines_to_local2(user_id, content):
    file_path = get_conversation_path(user_id)
    with open(file_path, "w", encoding="utf-8") as file:
        for c in content:
            print(c) 
            file.writelines(c)


#ファイルから読み込む
def load_lines(user_id):
    file_path = get_conversation_path(user_id)
    
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return lines