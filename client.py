from email import message
import socket
import threading
import json

# クライアントの設定
HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# username,roomname,messageを入力してサーバーに送信
# ユーザーから入力を受け取り、JSON形式に変換して送信
# "roomA"と" roomA"でも一緒にする必要があるから、空欄を削除する必要がある。
# username, roomname = input(
#     "Enter your username, room name: or message ").split(',')
user_input = input(
    "Enter your username, room name: or message ").split(',')
# 空欄を削除する必要がある。


# ここをusername,roomname2つの場合、mesage1つの場合に分けてsendすればいいのか。
# そしたら2回連続でusername,roomnameを提供した場合エラーを吐かせる必要がある。
# サーバー側でも1つか2つかを判断させる必要がある。

username = user_input[0].strip()
roomname = user_input[1].strip()
data = json.dumps([username, roomname])
# ここを起点にsend()ロープに持っていく
client.send(data.encode('utf-8'))
# サーバーからメッセージを受信する関数


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            # json.loads(message)
            print(message)
        except:
            # サーバーとの接続が切れた場合
            print("Connection lost.")
            client.close()
            break

# ユーザーの入力をサーバーに送信する関数


# def send():
#     while True:
#         message = input()
#         client.send(message.encode('utf-8'))
def send():
    while True:
        # user_input = input("Enter your message: ")
        user_input = input("")
        # if user_input.lower() == 'exit':
        #     break
        message_data = [{"message": user_input}]
        client.send(json.dumps(message_data).encode('utf-8'))


# def send実行 マルチクライアントに対応
send_thread = threading.Thread(target=send)
send_thread.start()
# def receive実行 マルチクライアントに対応
receive_thread = threading.Thread(target=receive)
receive_thread.start()
