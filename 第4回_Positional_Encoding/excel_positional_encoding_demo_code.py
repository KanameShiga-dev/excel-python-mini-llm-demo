import numpy as np
import pandas as pd

# 第4回 Positional Encoding
# Embeddingに位置情報を足すデモです。
# このコードは教材用であり、本物の大規模言語モデルのEmbeddingを再現するものではありません。

tokens_a = ["私", "は", "りんご", "を", "食べる"]
tokens_b = ["りんご", "を", "私", "は", "食べる"]

d_model = 4
max_len = max(len(tokens_a), len(tokens_b))

embedding_table = {
    "私": [0.20, 0.80, 0.10, 0.30],
    "は": [0.10, 0.20, 0.70, 0.20],
    "りんご": [0.90, 0.10, 0.30, 0.60],
    "を": [0.10, 0.30, 0.60, 0.10],
    "食べる": [0.70, 0.40, 0.20, 0.80],
}

def make_positional_encoding(max_len, d_model):
    pe = np.zeros((max_len, d_model))
    for pos in range(max_len):
        for i in range(0, d_model, 2):
            div_term = 10000 ** (i / d_model)
            pe[pos, i] = np.sin(pos / div_term)
            if i + 1 < d_model:
                pe[pos, i + 1] = np.cos(pos / div_term)
    return pe

positional_encoding = make_positional_encoding(max_len, d_model)

def make_input_df(tokens, sentence_name):
    return pd.DataFrame({
        "sentence": sentence_name,
        "position": list(range(len(tokens))),
        "token": tokens,
    })

def make_embedding_df():
    rows = []
    for token, vector in embedding_table.items():
        row = {"token": token}
        for i, value in enumerate(vector):
            row[f"dim_{i}"] = value
        rows.append(row)
    return pd.DataFrame(rows)

def make_position_df(pe):
    rows = []
    for pos in range(pe.shape[0]):
        row = {"position": pos}
        for i in range(pe.shape[1]):
            row[f"pe_{i}"] = round(float(pe[pos, i]), 3)
        rows.append(row)
    return pd.DataFrame(rows)

def make_final_df(tokens, sentence_name, pe):
    rows = []
    for pos, token in enumerate(tokens):
        embedding = np.array(embedding_table[token])
        final_vector = embedding + pe[pos]
        row = {"sentence": sentence_name, "position": pos, "token": token}
        for i, value in enumerate(final_vector):
            row[f"dim_{i}"] = round(float(value), 3)
        rows.append(row)
    return pd.DataFrame(rows)

def make_compare_df(tokens_a, tokens_b, pe):
    rows = []
    shared_tokens = sorted(set(tokens_a) & set(tokens_b), key=tokens_a.index)
    for token in shared_tokens:
        pos_a = tokens_a.index(token)
        pos_b = tokens_b.index(token)
        embedding = np.array(embedding_table[token])
        final_a = embedding + pe[pos_a]
        final_b = embedding + pe[pos_b]
        same_final = np.allclose(final_a, final_b)
        rows.append({
            "token": token,
            "文A position": pos_a,
            "文B position": pos_b,
            "Embeddingは同じ？": "同じ",
            "最終ベクトルは同じ？": "同じ" if same_final else "違う",
            "理由": "位置が同じ" if same_final else "足される位置ベクトルが違う",
        })
    return pd.DataFrame(rows)

input_a_df = make_input_df(tokens_a, "文A")
input_b_df = make_input_df(tokens_b, "文B")
embedding_df = make_embedding_df()
position_df = make_position_df(positional_encoding)
final_a_df = make_final_df(tokens_a, "文A", positional_encoding)
final_b_df = make_final_df(tokens_b, "文B", positional_encoding)
compare_df = make_compare_df(tokens_a, tokens_b, positional_encoding)

def add_section(df, section_name):
    result_df = df.copy()
    result_df.insert(0, "section", section_name)
    return result_df

all_outputs_df = pd.concat(
    [
        add_section(input_a_df, "01_INPUT_A"),
        add_section(input_b_df, "01_INPUT_B"),
        add_section(embedding_df, "02_EMBEDDING"),
        add_section(position_df, "03_POSITIONAL_ENCODING"),
        add_section(final_a_df, "04_ADD_RESULT_A"),
        add_section(final_b_df, "04_ADD_RESULT_B"),
        add_section(compare_df, "05_COMPARE"),
    ],
    ignore_index=True,
    sort=False,
)

# Python in ExcelではNaNが #NUM! と表示されることがあります。
# 表として見やすくするため、該当しない列は空欄にします。
all_outputs_df = all_outputs_df.fillna("")

def vector_text(values):
    return "[" + ", ".join(f"{float(v):.3f}" for v in values) + "]"

display_rows = []

for _, row in input_a_df.iterrows():
    display_rows.append({
        "section": "01_INPUT",
        "item": f"文A position {row['position']}",
        "token": row["token"],
        "value": f"{row['sentence']} / {row['position']}番目 / {row['token']}",
        "note": "入力文Aのtokenと位置",
    })

for _, row in input_b_df.iterrows():
    display_rows.append({
        "section": "01_INPUT",
        "item": f"文B position {row['position']}",
        "token": row["token"],
        "value": f"{row['sentence']} / {row['position']}番目 / {row['token']}",
        "note": "入力文Bのtokenと位置",
    })

for _, row in embedding_df.iterrows():
    display_rows.append({
        "section": "02_EMBEDDING",
        "item": f"{row['token']} のEmbedding",
        "token": row["token"],
        "value": vector_text([row["dim_0"], row["dim_1"], row["dim_2"], row["dim_3"]]),
        "note": "tokenごとに決まる単語の意味ベクトル",
    })

for _, row in position_df.iterrows():
    pos = int(row["position"])
    display_rows.append({
        "section": "03_POSITIONAL_ENCODING",
        "item": f"position {pos} の位置ベクトル",
        "token": "",
        "value": vector_text([row["pe_0"], row["pe_1"], row["pe_2"], row["pe_3"]]),
        "note": "positionごとに決まる場所のベクトル",
    })

for _, row in final_a_df.iterrows():
    display_rows.append({
        "section": "04_ADD_RESULT_A",
        "item": f"文A {row['token']} の最終ベクトル",
        "token": row["token"],
        "value": vector_text([row["dim_0"], row["dim_1"], row["dim_2"], row["dim_3"]]),
        "note": "Embedding + Positional Encoding",
    })

for _, row in final_b_df.iterrows():
    display_rows.append({
        "section": "04_ADD_RESULT_B",
        "item": f"文B {row['token']} の最終ベクトル",
        "token": row["token"],
        "value": vector_text([row["dim_0"], row["dim_1"], row["dim_2"], row["dim_3"]]),
        "note": "Embedding + Positional Encoding",
    })

for _, row in compare_df.iterrows():
    display_rows.append({
        "section": "05_COMPARE",
        "item": f"{row['token']} の位置違い比較",
        "token": row["token"],
        "value": f"文A: {row['文A position']}番目 / 文B: {row['文B position']}番目 / 最終ベクトル: {row['最終ベクトルは同じ？']}",
        "note": row["理由"],
    })

display_df = pd.DataFrame(display_rows)

# 既定では、見やすい縦長の確認表を表示します。
# dictを返さないため、Python in Excelで階層を1つずつ開く必要がありません。
# 数値列を横に広く見たい場合は、最後の行を all_outputs_df に変えて実行します。
# 個別の表だけを見たい場合は、最後の行を compare_df や embedding_df などに変えて実行します。
display_df
