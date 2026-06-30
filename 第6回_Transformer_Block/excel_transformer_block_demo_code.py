import pandas as pd
import numpy as np

tokens = ["今日", "猫", "ごはん", "食べる"]
dims = ["d1:意味", "d2:主語", "d3:動作", "d4:時制"]

X = np.array([
    [0.20, 0.10, 0.00, 0.70],
    [0.80, 0.90, 0.10, 0.20],
    [0.50, 0.20, 0.60, 0.10],
    [0.30, 0.10, 0.90, 0.40],
])

attention_output = np.array([
    [0.05, 0.00, 0.10, 0.20],
    [0.30, 0.20, 0.05, 0.00],
    [0.10, 0.05, 0.25, 0.05],
    [0.20, 0.10, 0.30, 0.10],
])

W1 = np.array([
    [0.5, -0.2, 0.1, 0.3, 0.2, -0.1],
    [0.1, 0.4, -0.3, 0.2, 0.1, 0.2],
    [0.2, 0.1, 0.5, -0.2, 0.3, 0.1],
    [-0.1, 0.3, 0.2, 0.4, -0.2, 0.2],
])
W2 = np.array([
    [0.3, 0.1, -0.2, 0.2],
    [-0.1, 0.4, 0.1, 0.0],
    [0.2, -0.2, 0.3, 0.1],
    [0.1, 0.2, -0.1, 0.3],
    [0.0, 0.1, 0.4, -0.2],
    [0.2, -0.1, 0.1, 0.2],
])

def layer_norm(a, eps=1e-5):
    mean = a.mean(axis=1, keepdims=True)
    var = ((a - mean) ** 2).mean(axis=1, keepdims=True)
    return (a - mean) / np.sqrt(var + eps)

def df(name, arr):
    out = pd.DataFrame(np.round(arr, 4), columns=dims)
    out.insert(0, "token", tokens)
    out.insert(1, "stage", name)
    return out

add1 = X + attention_output
norm1 = layer_norm(add1)
ffn_hidden = np.maximum(0, norm1 @ W1)
ffn_output = ffn_hidden @ W2
add2 = norm1 + ffn_output
block_output = layer_norm(add2)

flow_df = pd.concat([
    df("Input X", X),
    df("Attention Output", attention_output),
    df("Add1 = X + Attention", add1),
    df("Norm1 = LayerNorm(Add1)", norm1),
    df("FFN Output", ffn_output),
    df("Add2 = Norm1 + FFN", add2),
    df("Block Output", block_output),
], ignore_index=True)

trace_df = flow_df[flow_df["token"].eq("食べる")].reset_index(drop=True)

# Python in Excelで最後に表示したい表を選びます。
result_df = flow_df
# result_df = trace_df
# result_df = df("Block Output", block_output)

result_df
