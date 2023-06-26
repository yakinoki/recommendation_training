import numpy as np

# ユーザー/アイテムの評価値を表す行列
# 行はユーザー、列はアイテムに対応する
R = np.array([[3, 0, 4, 0], [0, 5, 0, 2], [1, 0, 0, 5], [0, 2, 4, 0]])

# ユーザー間の類似度と共通のアイテム数を計算する関数
def similarity(user1, user2):
    # ユーザーの評価値を取得
    ratings1 = R[user1, :]
    ratings2 = R[user2, :]

    # 共通のアイテムを抽出
    mask = np.logical_and(ratings1 != 0, ratings2 != 0)
    common_items = np.sum(mask)

    if common_items == 0:
        return 0, common_items

    # 共通のアイテムの評価値の差分を計算
    diff = ratings1[mask] - ratings2[mask]

    # ユーザー間の類似度を計算
    return 1 / (1 + np.linalg.norm(diff)), common_items

# 特定のユーザーに対するアイテムの評価値を予測する関数
def predict(user, item):
    # すでに評価済みの場合は評価値を返す
    if R[user, item] != 0:
        return R[user, item]

    # 類似度の高いユーザーの評価値を使用して予測値を計算
    sim_total = 0
    pred_total = 0
    for i in range(R.shape[0]):
        if i == user or R[i, item] == 0:
            continue
        sim, _ = similarity(user, i)
        sim_total += sim
        pred_total += sim * R[i, item]

    if sim_total == 0:
        return 0

    return pred_total / sim_total

# すべてのユーザー/アイテムの評価値を予測して行列で返す関数
def recommend():
    pred = np.zeros_like(R)
    for i in range(R.shape[0]):
        for j in range(R.shape[1]):
            pred[i, j] = predict(i, j)
    return pred

# MAP@Kを計算する関数
def calculate_map(pred, K):
    num_users = pred.shape[0]
    average_precision = []
    for user in range(num_users):
        true_positives = 0
        precision = 0
        for item in range(K):
            top_items = np.argsort(pred[user, :])[::-1][:K]
            if R[user, top_items[item]] != 0:
                true_positives += 1
                precision += true_positives / (item + 1)
        average_precision.append(precision / min(K, np.sum(R[user, :] != 0)))
    return np.mean(average_precision)

# 推薦結果とMAP@Kを出力
pred = recommend()
K = 3  # 上位K件のアイテムを評価
map_at_k = calculate_map(pred, K)
print("MAP@{}: {:.4f}".format(K, map_at_k))
