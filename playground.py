import json


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
