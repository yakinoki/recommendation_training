import csv
from collections import defaultdict

# アクセスログのサンプルデータを作成
access_logs = [
    ['ユーザー1', 'アイテムA'],
    ['ユーザー1', 'アイテムB'],
    ['ユーザー1', 'アイテムC'],
    ['ユーザー2', 'アイテムA'],
    ['ユーザー2', 'アイテムC'],
    ['ユーザー3', 'アイテムB'],
    ['ユーザー3', 'アイテムC'],
    ['ユーザー4', 'アイテムA'],
    ['ユーザー4', 'アイテムB'],
    ['ユーザー4', 'アイテムC']
]

# CSVファイルにアクセスログを書き込む
with open('access_logs.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(access_logs)

# アクセスログのCSVファイルからデータを読み込む
with open('access_logs.csv', 'r') as file:
    reader = csv.reader(file)
    access_logs = list(reader)

# ユーザーごとのアクセス履歴を辞書として格納
user_history = defaultdict(list)
for row in access_logs:
    user = row[0]
    item = row[1]
    user_history[user].append(item)

# ユーザーの過去のアクセス履歴を基にレコメンデーションを行う
def recommend_items(user):
    # ユーザーのアクセス履歴を取得
    history = user_history[user]

    # レコメンデーション対象のアイテムを抽出
    all_items = set()
    for items in user_history.values():
        all_items.update(items)

    # レコメンデーション対象のアイテムから過去にアクセスしたアイテムを除外
    recommend_items = list(all_items - set(history))

    return recommend_items

# レコメンデーションの実行
user = 'ユーザー1'
recommendations = recommend_items(user)

# 結果の表示
print(f"ユーザー {user} に対するレコメンデーション:")
for item in recommendations:
    print(item)
