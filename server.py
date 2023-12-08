from email import message
import socket
import json
from unicodedata import name
from urllib import response  # 配列を送信するため

# サーバーのホストとポート
server_host = '0.0.0.0'
server_port = 9001

# ソケットの作成
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# サーバーのアドレスとポートにバインド
server_socket.bind((server_host, server_port))

# 接続の待機
server_socket.listen(1)
print('Waiting for incoming connections...')

# クライアントからの接続を受け入れる
client_socket, client_address = server_socket.accept()
print(f'Connected to {client_address}')

# 送信の関数#


def send_data(data):
    client_socket.send(data.encode())
# 受信の関数#


def receive_data(buffer_size=1024):
    return client_socket.recv(buffer_size).decode()


chat_rooms = {}


def command_handler(command_arr):
    last_arr = command_arr[-1]
    store_data = "store_data.txt"
    target = command_arr[0]
    hashmap_data = {}
    ## create ##
    if last_arr == "create":
        print("last arr is create")
        with open(store_data, 'a') as room_data:  # 'a' モードでファイルを開くことで追記モードになる
            room_data.write(f'\n{command_arr[0]}')
        # これすでにファイル内に書かれてから実行されるから、必ずif foundが実行される
        with open(store_data, "r") as stored_room_data:
            found = any(target in line for line in stored_room_data)
            if found:
                print(f"{target} found")
            else:
                print(f"room:{command_arr[0]} doesnot exist")
                # send_data(f'you joined {command_arr[0]} Lets chat!')
                # send to client あとinput()も作る
                print("room created!")
        # send to client
        message = f"{command_arr[0]} created. message from server.py"
        hashmap_data["create"] = message
        # send_data(json.dumps(hashmap_data))

    ## join ##
    elif last_arr == "join":
        chat_room_name = command_arr[0]
        user = command_arr[1]
        print("join!")

        with open(store_data, "r") as stored_room_data:
            found = any(target in line for line in stored_room_data)
            if found:
                message = f"{user} successfuly joined {target}!"
                hashmap_data["join"] = message
            else:
                print(f"room:{chat_room_name} doesnot exist")

    ## send ##
    elif last_arr == "send":
        print("send")
    ## help ##
    elif last_arr == "help":
        print("help!")
    ## exit ##
    elif last_arr == "exit":
        print("exit")
        client_socket.close()
        server_socket.close()
    ## 例外 ##
    else:
        print("tf?")

    # {"create":message, "join":something,"help":something ~}
    send_data(json.dumps(hashmap_data))

####### command_handle ######################


######## received text##########
while True:
    # receive
    received_text = receive_data()
    received_text_arr = json.loads(received_text)
    print(received_text_arr)
    command_handler(received_text_arr)
    break  # exitが入力されたら通信終わる。これはおまけ。
######## received text##########

# close
while True:
    user_input = input("Enter 'exit' to close connection: ")
    if user_input.lower() == "exit":
        # ユーザーが 'exit' と入力した場合、通信を終了する
        # ここに通信を終了するためのコードを追加する
        break  # 通信を終了するためループから抜ける
    client_socket.close()
    server_socket.close()


#########
# - createの後にjoinコマンドを打ったら機能していない->ループが機能していない
# - createコマンドの中身を実装していく
