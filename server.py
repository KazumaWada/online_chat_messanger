import socket
import threading
import json

# サーバーの設定
HOST = '127.0.0.1'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# 接続されたクライアントとユーザー名を格納する辞書
clients = {}
chatroom = {}
rooms = {}


class Chatroom:
    def __init__(self, name):
        self.name = name


class User:
    def __init__(self, name):
        self.name = name

# メッセージを受信し、他のクライアントに転送する関数

# room:chatroomをインスタンス化する変数
# rooms: chatroomたちを格納するhashmap


def handle_client(client_socket, addr):
    try:
        # ユーザー名をクライアントから受け取る
        # 配列で受け取れるようにする{username,roomname,message}
        ini_data_str = client_socket.recv(1024).decode('utf-8')
        ini_data_arr = json.loads(ini_data_str)
        ## 1回目のrecv##
        # 新規chatroom
        user = User(ini_data_arr[0])
        room = Chatroom(ini_data_arr[1])

        if ini_data_arr[1] not in rooms:
            # 部屋のhashmapを作る
            rooms[ini_data_arr[1]] = []
            print(f"{user.name} connected from {addr}. created {room.name}")
        # 既存のchatroomにjoin
        else:
            print(f"{user.name} connected from {addr}. joined {room.name}")

        # 特定の部屋にユーザーを追加する
        rooms[ini_data_arr[1]].append(user.name)

        # ユーザー名を辞書に追加
        # ここを全員格納するのではなく、room名と紐付けて格納する必要がある
        clients[client_socket] = (user.name, room.name)
        print("before while true")
        ## 2回目のrecv##
        while True:
            print("inside of while")
            message = client_socket.recv(1024).decode('utf-8')
            message_arr = json.loads(message)
            # 多分送ってくる配列と取得する配列が違う??

            if not message_arr[0]:
                print("no message")
                # クライアントが切断された場合
                remove_client(client_socket)
                break
            else:
                print("inside of while/whie true/else")
                for client_sock, (username_client, roomname_client) in clients.items():
                    # 同じ部屋かつ違うユーザー(ソケット)
                    if roomname_client == room.name and client_sock != client_socket:
                        message_data = {f"{user.name} said": message_arr[0]}
                        client_sock.send(json.dumps(
                            message_data).encode('utf-8'))

                # クライアント自身にも送信する
                message_data_to_myself = {f"You said": message_arr[0]}
                client_socket.send(json.dumps(
                    message_data_to_myself).encode('utf-8'))

    except:
        print("error")
        remove_client(client_socket)


def remove_client(client_socket):
    if client_socket in clients:
        # clients = []
        # hashmapの値は2つ格納する事ができる
        # clients[client_socket] = (user.name, ini_data_arr[1])
        user, room = clients[client_socket]
        print(f"{user} disconnected from room {room}")
        del clients[client_socket]
        # userをroomから削除する。
        print(rooms[room])
        rooms[room].remove(user)
        if len(rooms[room]) == 0:
            del rooms[room]


# クライアントの接続を待ち受けるループ
# handle_clientを呼び出しマルチスレッドで待ち受ける
while True:
    client_socket, addr = server.accept()
    clients[client_socket] = ("", "")  # 初期値

    # 各クライアントごとにスレッドを起動
    client_thread = threading.Thread(
        target=handle_client, args=(client_socket, addr))
    client_thread.start()

# 続き
# これだと簡単すぎる。
# チャットルームを作成、joinの機能を作って次に行く
#########################################
# {roomanema} :join #新規作成でも同じコマンド!
# clientは一度に一つの部屋のみ参加できる[後]
# % roomname messageでサーバに送信する
# ↑送信する前に、そのclientがその部屋に参加しているか確認する
##########################################
