import numpy as np
import pandas as pd

raw_token_a = xl("'01_INPUT'!B6")
raw_token_b = xl("'01_INPUT'!B7")
raw_mode = xl("'01_INPUT'!B8")
raw_map_x = xl("'01_INPUT'!B9")
raw_map_y = xl("'01_INPUT'!B10")

token_a = "犬" if raw_token_a is None or pd.isna(raw_token_a) else str(raw_token_a).strip()
token_b = "猫" if raw_token_b is None or pd.isna(raw_token_b) else str(raw_token_b).strip()
mode = "Vector Compare" if raw_mode is None or pd.isna(raw_mode) else str(raw_mode).strip()

data = [
    {"token": "犬", "category": "動物", "dim_1_living": 0.90, "dim_2_vehicle": 0.05, "dim_3_action": 0.05, "dim_4_system": 0.00},
    {"token": "猫", "category": "動物", "dim_1_living": 0.85, "dim_2_vehicle": 0.05, "dim_3_action": 0.05, "dim_4_system": 0.00},
    {"token": "車", "category": "乗り物", "dim_1_living": 0.05, "dim_2_vehicle": 0.90, "dim_3_action": 0.05, "dim_4_system": 0.00},
    {"token": "電車", "category": "乗り物", "dim_1_living": 0.05, "dim_2_vehicle": 0.85, "dim_3_action": 0.05, "dim_4_system": 0.00},
    {"token": "保存", "category": "操作", "dim_1_living": 0.00, "dim_2_vehicle": 0.00, "dim_3_action": 0.90, "dim_4_system": 0.50},
    {"token": "削除", "category": "操作", "dim_1_living": 0.00, "dim_2_vehicle": 0.00, "dim_3_action": 0.85, "dim_4_system": 0.45},
    {"token": "DB", "category": "システム", "dim_1_living": 0.00, "dim_2_vehicle": 0.00, "dim_3_action": 0.20, "dim_4_system": 0.95},
    {"token": "ファイル", "category": "システム", "dim_1_living": 0.00, "dim_2_vehicle": 0.00, "dim_3_action": 0.25, "dim_4_system": 0.85},
]

df = pd.DataFrame(data)
df.insert(0, "token_id", range(1, len(df) + 1))

dim_cols = ["dim_1_living", "dim_2_vehicle", "dim_3_action", "dim_4_system"]
map_x = "dim_1_living" if raw_map_x is None or pd.isna(raw_map_x) else str(raw_map_x).strip()
map_y = "dim_2_vehicle" if raw_map_y is None or pd.isna(raw_map_y) else str(raw_map_y).strip()

if map_x not in dim_cols:
    map_x = "dim_1_living"
if map_y not in dim_cols:
    map_y = "dim_2_vehicle"

def cosine_similarity(vec1, vec2):
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm1 * norm2))

def get_row(token):
    if token in df["token"].values:
        return df[df["token"] == token].iloc[0]
    return df.iloc[0]

row_a = get_row(token_a)
row_b = get_row(token_b)

vec_a = row_a[dim_cols].to_numpy(dtype=float)
vec_b = row_b[dim_cols].to_numpy(dtype=float)
similarity = cosine_similarity(vec_a, vec_b)

token_id_df = df[["token_id", "token", "category"]].copy()
token_id_df["note"] = "token IDは番号であり、意味の近さはこの表だけでは分からない"

embedding_df = df.copy()

compare_rows = [
    {"item": "token", "token A": row_a["token"], "token B": row_b["token"], "note": "比較対象"},
    {"item": "token_id", "token A": row_a["token_id"], "token B": row_b["token_id"], "note": "ID番号"},
    {"item": "category", "token A": row_a["category"], "token B": row_b["category"], "note": "教材用の分類"},
]

for col in dim_cols:
    compare_rows.append({
        "item": col,
        "token A": round(float(row_a[col]), 3),
        "token B": round(float(row_b[col]), 3),
        "note": "Embeddingの1次元",
    })

compare_rows.append({
    "item": "cosine_similarity",
    "token A": round(similarity, 3),
    "token B": round(similarity, 3),
    "note": "1に近いほどベクトルの向きが似ている",
})

compare_df = pd.DataFrame(compare_rows)

vectors = df[dim_cols].to_numpy(dtype=float)
sim_matrix = np.zeros((len(df), len(df)))

for i in range(len(df)):
    for j in range(len(df)):
        sim_matrix[i, j] = cosine_similarity(vectors[i], vectors[j])

sim_df = pd.DataFrame(np.round(sim_matrix, 3), columns=df["token"])
sim_df.insert(0, "token", df["token"])

map_df = df[["token_id", "token", "category", map_x, map_y]].copy()
map_df = map_df.rename(columns={map_x: "x_axis", map_y: "y_axis"})
map_df["x_axis_name"] = map_x
map_df["y_axis_name"] = map_y
map_df["note"] = "選んだ2つの次元だけを使った簡易マップ"

outputs = {
    "Token ID": token_id_df,
    "Embedding Table": embedding_df,
    "Vector Compare": compare_df,
    "Similarity Matrix": sim_df,
    "Map View": map_df,
}

outputs[mode] if mode in outputs else compare_df
