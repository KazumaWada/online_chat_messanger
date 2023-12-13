import socket
import json  # 配列を送信するため

# サーバーのホストとポート
server_host = '127.0.0.1'
server_port = 9001

# ソケットの作成
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# サーバーに接続
client_socket.connect((server_host, server_port))

# 送信の関数#


def send_data(data):
    client_socket.send(data.encode())
# 受信の関数#


def receive_data(buffer_size=1024):
    return client_socket.recv(buffer_size).decode()


def receive_data_handler(hashmap):
    # 送信した最後のコマンドの内容の処理が成功したかここで表示される
    if "create" in hashmap.keys():
        # {"create": message}
        # "create"に対応する値を表示する
        print(hashmap.get("create"))
    elif "join" in hashmap.keys():
        print(hashmap.get("join"))
    elif "send" in hashmap.keys():
        print(hashmap.get("send"))
    elif "help" in hashmap.keys():
        print(hashmap.get("help"))
    elif "exit" in hashmap.keys():
        print(hashmap.get("exit"))
    else:
        print("else")


while True:

    # send
    # こっちは送信と受信をし続けている。serverは受信と送信をし続けているか?
    send_chat_message = input(

        '/////////////////////////////////////////////////\
    \n- create room->[room name,message-size,initial message to chatroom,create \
    \n- join room->[room,user_name,join]\
    \n- text to room->[message,send]\
    \n- type"help"  if you want to know how this works:\
    \n- exit\
    \n/////////////////////////////////////////////////\
    \n:')

    send_chat_message_arr = send_chat_message.split(',')
    send_data(json.dumps(send_chat_message_arr))

    # receive
    hashmap_data = receive_data()
    hashmap = json.loads(hashmap_data)
    if "create" in hashmap.keys() or "join" in hashmap.keys() or "send" in hashmap.keys():

        receive_data_handler(hashmap)
    else:
        print("commmand is not valid")
        break

# close
while True:
    user_input = input("→ Enter 'exit' to close connection: ")
    if user_input.lower() == "exit":
        break
client_socket.close()


# 最初に{roomname}:{message-size}:{message}をサーバーに送信. messageは参加した全ての人に送信するメッセージ("welcome to war room" etc)
# ↑送信者がすでにchatroomに参加している必要がある。
# chatroom作成->自動的にそのユーザーがホストになる。(という事はユーザーClassも作成する必要がある)
# chatroom作成->{"chatroom name" : ChatRoom(参加者,"chatroom name",別のハッシュマップ)}
# ChatClient(クライアントのアドレス、ポート、その他の必要なデータ)
# クライアントは一度に一部屋のみ参加可能
# {アドレス&ポート : chatroom}で、ChatClientを特定する事ができる
# {roomname}:joinで参加(その後にvalidationを通過したらmessageがそのユーザーに送られる)
# メッセージをチャットルーム内に送信できる機能を作る。(forループで全員に同じメッセージを送るとか)


# Online Chat Messenger
# クライアントがチャットルームを作成し、参加することができるサービスを作成します。
# 各チャットルームは一意のキーで識別されます。このキーはチャットルームの識別子として機能し、他のユーザーがそのチャットルームに参加することを可能にします。
# 新しいチャットルームを作成する際には、タイトルと最大参加者数を指定する必要があります。
# このサービスは、チャットルームの作成中にデータが失われないように、ポート A の TCP 接続を使用する必要があります。
# チャットルームが作成されると、作成したクライアントは自動的に UDP でチャットルームに接続され、ホストとして指定されます。
# チャットルームは、<string, ChatRoom> のハッシュマップとして実装する必要があり、ChatRoom は参加者、<string, ChatClient> オブジェクトの別のハッシュマップ、
# サイズやタイトルなどのチャットルーム情報を含むオブジェクトとなります。
# ChatClient は、クライアントのアドレスとポート、およびクライアントの追加データを含むオブジェクトです。
# アドレスとポートを連結して ChatRoom のキーとすることで、ChatClient を一意に特定することができます。
# 各クライアントは一度に 1 つのチャットルームにしか参加できず、チャットルームの参加者数はルーム作成時に指定した最大人数を超えることはできません。
# サーバに送信するメッセージは、{roomname}:{message-size}:{message} というプレフィックスで始めます。roomname は参加した部屋を示す文字列、
# message-size はメッセージのサイズ、message はチャットに参加した全ての人に送信するメッセージです。メッセージの送信時に、
# 送信者がサーバ内のチャットルームに参加していることを確認する必要があります。

# チャットルームに参加する場合は、{roomname}:join を含むメッセージをサーバに送信します。
# メッセージをチャットルーム内の他の人に転送する場合は、単純な for ループを使うか、Python の asyncio ライブラリのような非同期ツールを使って
# 転送することができます。
