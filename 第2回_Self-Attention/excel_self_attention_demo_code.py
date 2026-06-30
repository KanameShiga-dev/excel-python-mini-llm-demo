import numpy as np
import pandas as pd

raw_text = xl("'01_INPUT'!B6")
raw_mode = xl("'01_INPUT'!B7")
input_text = "注文履歴 は 正本 DB に 保存 する" if raw_text is None or pd.isna(raw_text) else str(raw_text)
mode = "Attention Weight" if raw_mode is None or pd.isna(raw_mode) else str(raw_mode).strip()
tokens = [t for t in input_text.split() if t.strip()][:12]
tokens = tokens if len(tokens) else ["(空)"]
dim = 4
pos = np.arange(1, len(tokens) + 1).reshape(-1, 1)
dims = np.arange(1, dim + 1).reshape(1, -1)
code_sums = np.array([sum(ord(ch) for ch in token) for token in tokens]).reshape(-1, 1)
emb = 0.12 + (((code_sums + dims * 17 + pos * 11) % 31) / 30) * 0.62
denominator = 100 ** (((dims - 1) // 2) / dim)
angle = pos / denominator
pe = np.where((dims - 1) % 2 == 0, np.sin(angle) * 0.12, np.cos(angle) * 0.12)
x = emb + pe
wq = np.array([[0.80,0.10,-0.20,0.30],[0.00,0.70,0.25,-0.10],[0.20,-0.30,0.60,0.10],[-0.10,0.20,0.10,0.70]])
wk = np.array([[0.70,-0.10,0.10,0.20],[0.20,0.60,-0.20,0.10],[-0.10,0.30,0.70,0.00],[0.10,0.00,0.20,0.80]])
wv = np.array([[0.60,0.20,0.00,-0.10],[0.10,0.70,0.20,0.00],[0.00,-0.10,0.80,0.20],[0.20,0.10,0.10,0.60]])
q = x @ wq
k = x @ wk
v = x @ wv
boost = np.array([[2.4 if qt == "保存" and kt == "DB" else 1.6 if qt == "DB" and kt == "正本" else 1.2 if qt == "正本" and kt == "注文履歴" else 1.5 if qt == "する" and kt == "保存" else 2.4 if qt == "確認" and kt == "請求書" else 1.2 if qt == "AI" and kt == "確認" else 1.8 if qt == "学ぶ" and kt == "AI" else 1.4 if qt == "学ぶ" and kt == "しくみ" else 0.25 if qt == kt else 0.0 for kt in tokens] for qt in tokens], dtype=float)
scores = q @ k.T / np.sqrt(dim) + boost
exp_scores = np.exp(scores - np.max(scores, axis=1, keepdims=True))
weights = exp_scores / exp_scores.sum(axis=1, keepdims=True)
context = weights @ v
strongest = [tokens[int(np.argmax(row))] for row in weights]
token_df = pd.DataFrame({"position": range(1, len(tokens)+1), "token": tokens, "token_id": range(1, len(tokens)+1), "note": ["空白区切りtoken"] * len(tokens)})
emb_df = pd.DataFrame(np.round(np.hstack([emb, pe, x]), 3), columns=["dim_1","dim_2","dim_3","dim_4","positional_1","positional_2","positional_3","positional_4","input_vector_1","input_vector_2","input_vector_3","input_vector_4"])
emb_df.insert(0, "token", tokens)
qkv_df = pd.DataFrame(np.round(np.hstack([q, k, v]), 3), columns=["Q1","Q2","Q3","Q4","K1","K2","K3","K4","V1","V2","V3","V4"])
qkv_df.insert(0, "token", tokens)
score_df = pd.DataFrame(np.round(scores, 3), columns=tokens)
score_df.insert(0, "見る側 / 見られる側", tokens)
weight_df = pd.DataFrame(np.round(weights, 3), columns=tokens)
weight_df.insert(0, "見る側 / 見られる側", tokens)
weight_df["行合計"] = np.round(weights.sum(axis=1), 3)
ctx_df = pd.DataFrame(np.round(context, 3), columns=["context_1","context_2","context_3","context_4"])
ctx_df.insert(0, "token", tokens)
ctx_df["一番強く見ているtoken"] = strongest
ctx_df["解釈メモ"] = [f"{token} は {target} を比較的強く参照" for token, target in zip(tokens, strongest)]
outputs = {"token一覧": token_df, "embedding": emb_df, "Q/K/V": qkv_df, "Attention Score": score_df, "Attention Weight": weight_df, "Context Vector": ctx_df}
outputs[mode] if mode in outputs else outputs["Attention Weight"]
