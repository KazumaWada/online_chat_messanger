from email import message
import socket
import json
from unicodedata import name
from urllib import response

from playground import find_data  # 配列を送信するため

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


class ChatRoom:
    # ここのchatroomにどのユーザーがいるか知るために、
    # chatroom class内にUserを入れた方が良いと思う。
    def __init__(self, name):
        self.name = name
        self.users = {}

    def add_user(self, user):
        # user.name->class User.nameから来ている。
        self.users[user.name] = user
        # self.users{admin:"admin"}

    def get_user(self, name):
        # hashmapのget
        return self.users.get(name)


class User:
    def __init__(self, name):
        self.name = name

# # 新しいチャットルームを作成
# python_chat = ChatRoom("Python Chat")

# # ユーザーを作成
# user1 = User("Alice")
# user2 = User("Bob")

# # ユーザーをチャットルームに追加
# python_chat.add_user(user1)
# python_chat.add_user(user2)

# # チャットルームからユーザーを取得して表示
# found_user = python_chat.get_user("Alice")
# if found_user:
#     print(f"User found: {found_user.username}")
# else:
#     print("User not found")


def find_data(data):
    file_path = "chatroom_data.txt"

    # テキストデータを読み取って、辞書形式に変換する
    hashmap = {}
    with open(file_path, "r") as file:
        for line in file:
            # 空白を削除
            # 1行だからhashmapを1行にして書く必要がある
            line = line.strip()
            if line:
                room, user, user_string = line.split(":")
                # まだ空白があるらしいから削除
                room = room.strip()
                user = user.strip()
                user_string = user_string.strip()
                # 部屋が存在しなかったら辞書に登録
                if room not in hashmap:
                    hashmap[room] = {}
                # key, value = user.strip()
                key, value = user, user_string
                hashmap[room][key] = value

    # JSON形式に変換する
    json_data = json.dumps(hashmap, indent=2)
    json_data = json.loads(json_data)
    # if json_data[room_name] == exit

    # JSONデータを出力する
    # print(json_data)
    # print(json_data["good_room"]["admin"])  # {'admin': 'admin'}
    if json_data[data]:
        return True
    else:
        return False


def command_handler(command_arr):
    last_arr = command_arr[-1]
    store_data = "store_data.txt"
    target = command_arr[0]
    hashmap_message_data = {}
    hashmap_room_data = {}
    hashmap_user_data = {}

    ## create ##
    if last_arr == "create":
        room_name = command_arr[0]
        admin = "admin"

        # validation

        # def store_chatroom_data(room_name):
        with open("chatroom_data.txt", 'a') as chatroom_data:  # 'a' モードでファイルを開くことで追記モードになる
            chatroom_data.write(f'\n{room_name}: {admin}: admin\n')
        message = (
            f"room {room_name} created you are "
            f"admin. message from server.py"
        )
        hashmap_message_data["create"] = message

    ## join ##
    # [room,user_name,join]
    elif last_arr == "join":
        chatroom_name = command_arr[0]
        user = command_arr[1]

        if find_data(chatroom_name):
            message = f"{user} successfuly joined {target}!"
            hashmap_message_data["join"] = message
        else:
            print(f"room:{chatroom_name} doesnot exist")

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
    send_data(json.dumps(hashmap_message_data))

####### command_handle ######################


######## received text##########
while True:
    # receive
    received_text = receive_data()
    received_text_arr = json.loads(received_text)
    print(received_text_arr)
    # ここで関数に飛んで抜けてしまってない??
    command_handler(received_text_arr)
    if received_text_arr[-1] == "exit":
        break
######## received text##########


# close
client_socket.close()
server_socket.close()


##### やる事####
# 続き
# joinのvalidationができた!!!
# joinのlogicを作っていく。->まず、userを.txtのデータに追加する
