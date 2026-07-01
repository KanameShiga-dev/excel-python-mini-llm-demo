import numpy as np
import pandas as pd

# 第5回 Multi-Head Attention
# Q/K/V -> score -> softmax -> output -> concat を実際に計算します。

input_x_source_df = xl("'01_INPUT_X'!A3:F8", headers=True).dropna(how="all")
head1_weight_source_df = xl("'02_WEIGHTS_HEAD1'!A3:D15", headers=True).dropna(how="all")
head2_weight_source_df = xl("'07_WEIGHTS_HEAD2'!A3:D15", headers=True).dropna(how="all")

tokens = input_x_source_df["token"].astype(str).tolist()
x_columns = [c for c in input_x_source_df.columns if str(c).startswith("x")]
X = input_x_source_df[x_columns].astype(float).to_numpy()

def weight_matrices(weight_df):
    out_columns = [c for c in weight_df.columns if str(c).startswith("out_")]
    return {
        matrix_name: weight_df[weight_df["matrix"].eq(matrix_name)][out_columns].astype(float).to_numpy()
        for matrix_name in ["Wq", "Wk", "Wv"]
    }

W = {
    "Head 1": weight_matrices(head1_weight_source_df),
    "Head 2": weight_matrices(head2_weight_source_df),
}
dk = W["Head 1"]["Wk"].shape[1]

def r(v):
    return round(float(v), 4)

def vt(a):
    return "[" + ", ".join(f"{float(v):.4f}" for v in a) + "]"

def sm(score):
    e = np.exp(score - score.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True), e

def calc(h):
    q, k, v = X @ W[h]["Wq"], X @ W[h]["Wk"], X @ W[h]["Wv"]
    dot = q @ k.T
    score = dot / np.sqrt(dk)
    weight, exp_score = sm(score)
    out = weight @ v
    return {"Q": q, "K": k, "V": v, "dot": dot, "score": score,
            "exp_score": exp_score, "weight": weight, "output": out}

R = {h: calc(h) for h in W}

input_x_df = pd.DataFrame(
    [{"position": i, "token": t, "x0": X[i,0], "x1": X[i,1], "x2": X[i,2], "x3": X[i,3]}
     for i, t in enumerate(tokens)]
)

def weights_df(h):
    return pd.DataFrame([
        {"matrix": m, "input_dim": f"x{i}", "out_0": A[i,0], "out_1": A[i,1]}
        for m, A in W[h].items() for i in range(4)
    ])

def qkv_df(h):
    rows = []
    for kind, wm in [("Q", "Wq"), ("K", "Wk"), ("V", "Wv")]:
        A = R[h][kind]
        for i, t in enumerate(tokens):
            rows.append({"kind": kind, "position": i, "token": t,
                         "dim_0": r(A[i,0]), "dim_1": r(A[i,1]),
                         "formula": f"{kind}=X@{wm}"})
    return pd.DataFrame(rows)

def score_df(h):
    A = R[h]
    return pd.DataFrame([
        {"query_pos": i, "query_token": qt, "key_pos": j, "key_token": kt,
         "dot": r(A["dot"][i,j]), "score": r(A["score"][i,j]),
         "formula": f"Q[{i}]・K[{j}]/sqrt(2)"}
        for i, qt in enumerate(tokens) for j, kt in enumerate(tokens)
    ])

def softmax_df(h):
    A = R[h]
    return pd.DataFrame([
        {"query_pos": i, "query_token": qt, "key_pos": j, "key_token": kt,
         "score": r(A["score"][i,j]), "exp_score": r(A["exp_score"][i,j]),
         "attention_weight": r(A["weight"][i,j])}
        for i, qt in enumerate(tokens) for j, kt in enumerate(tokens)
    ])

def output_df(h):
    A = R[h]["output"]
    return pd.DataFrame([
        {"position": i, "token": t, "out_0": r(A[i,0]), "out_1": r(A[i,1]),
         "formula": "output=attention_weight row@V"}
        for i, t in enumerate(tokens)
    ])

def concat_df_make():
    h1, h2 = R["Head 1"]["output"], R["Head 2"]["output"]
    rows = []
    for i, t in enumerate(tokens):
        c = np.r_[h1[i], h2[i]]
        rows.append({"position": i, "token": t, "head1_0": r(h1[i,0]),
                     "head1_1": r(h1[i,1]), "head2_0": r(h2[i,0]),
                     "head2_1": r(h2[i,1]), "concat_vector": vt(c),
                     "formula": "concat=[Head1 output, Head2 output]"})
    return pd.DataFrame(rows)

def focus_df(qp=4):
    rows = []
    for h in ["Head 1", "Head 2"]:
        A = R[h]
        rows += [
            {"section": "Q", "head": h, "query": tokens[qp], "key": "",
             "value": vt(A["Q"][qp]), "formula": f"Q[{qp}]=X[{qp}]@Wq"},
            {"section": "K", "head": h, "query": tokens[qp], "key": "all",
             "value": "各key tokenのK", "formula": "K=X@Wk"},
            {"section": "V", "head": h, "query": tokens[qp], "key": "all",
             "value": "各key tokenのV", "formula": "V=X@Wv"},
        ]
        rows += [{"section": "score", "head": h, "query": tokens[qp], "key": kt,
                  "value": r(A["score"][qp,j]), "formula": f"Q[{qp}]・K[{j}]/sqrt(2)"}
                 for j, kt in enumerate(tokens)]
        rows += [{"section": "softmax", "head": h, "query": tokens[qp], "key": kt,
                  "value": r(A["weight"][qp,j]), "formula": "exp(score)/sum(row)"}
                 for j, kt in enumerate(tokens)]
        rows.append({"section": "output", "head": h, "query": tokens[qp], "key": "",
                     "value": vt(A["output"][qp]), "formula": "weight row@V"})
    c = np.r_[R["Head 1"]["output"][qp], R["Head 2"]["output"][qp]]
    rows.append({"section": "concat", "head": "Head 1 + Head 2", "query": tokens[qp],
                 "key": "", "value": vt(c), "formula": "concat=[Head1, Head2]"})
    return pd.DataFrame(rows)

weights_head1_df = weights_df("Head 1")
qkv_head1_df = qkv_df("Head 1")
score_head1_df = score_df("Head 1")
softmax_head1_df = softmax_df("Head 1")
output_head1_df = output_df("Head 1")
weights_head2_df = weights_df("Head 2")
qkv_head2_df = qkv_df("Head 2")
score_head2_df = score_df("Head 2")
softmax_head2_df = softmax_df("Head 2")
output_head2_df = output_df("Head 2")
concat_df = concat_df_make()
focus_trace_df = focus_df(4)

# 表示したいDataFrameをここで選ぶ
python_result_df = focus_trace_df.copy()
# python_result_df = concat_df.copy()
# python_result_df = qkv_head1_df.copy()
# python_result_df = score_head1_df.copy()
# python_result_df = softmax_head1_df.copy()
# python_result_df = output_head1_df.copy()
# python_result_df = qkv_head2_df.copy()
# python_result_df = score_head2_df.copy()
# python_result_df = softmax_head2_df.copy()
# python_result_df = output_head2_df.copy()
python_result_df
