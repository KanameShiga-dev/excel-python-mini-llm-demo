import pandas as pd
import numpy as np

context_source_df = xl("'01_INPUT'!A6:B12", headers=True).dropna(how="all")
candidate_source_df = xl("'01_INPUT'!E6:F12", headers=True).dropna(how="all")
settings_source_df = xl("'01_INPUT'!A15:C18", headers=True).dropna(how="all")

context_tokens = context_source_df["token"].dropna().astype(str).tolist()
vocab = candidate_source_df["candidate_token"].astype(str).tolist()
logits = candidate_source_df["logit"].astype(float).to_numpy()
settings = dict(zip(settings_source_df["parameter"].astype(str), settings_source_df["value"]))
temperature = float(settings.get("temperature", 1.0))
temperatures = [0.7, temperature, 1.5]
top_k = int(float(settings.get("top_k", 3)))
seeds = [int(s.strip()) for s in str(settings.get("seed", "11, 22, 33, 44, 55")).split(",") if s.strip()]

def softmax(values, temperature=1.0):
    scaled = values / temperature
    shifted = scaled - scaled.max()
    exps = np.exp(shifted)
    return exps / exps.sum()

def sample_from_probs(tokens, probabilities, seed):
    rng = np.random.default_rng(seed)
    r = float(rng.random())
    cumulative = np.cumsum(probabilities)
    picked_index = int(np.searchsorted(cumulative, r, side="right"))
    picked_index = min(picked_index, len(tokens) - 1)
    return tokens[picked_index], r

score_rows = []
temperature_rows = []
for temp in temperatures:
    probs = softmax(logits, temp)
    order = np.argsort(-probs)
    for rank, idx in enumerate(order, start=1):
        row = {
            "temperature": temp,
            "rank": rank,
            "candidate_token": vocab[idx],
            "logit": round(float(logits[idx]), 4),
            "scaled_logit": round(float(logits[idx] / temp), 4),
            "probability": round(float(probs[idx]), 4),
        }
        temperature_rows.append(row)
        if temp == 1.0:
            score_rows.append({k: row[k] for k in ["rank", "candidate_token", "logit", "scaled_logit", "probability"]})

base_probs = softmax(logits, 1.0)
base_order = np.argsort(-base_probs)
greedy_token = vocab[int(base_order[0])]

top_indices = base_order[:top_k]
top_probs = base_probs[top_indices] / base_probs[top_indices].sum()
top_k_rows = []
for rank, (idx, adjusted_prob) in enumerate(zip(top_indices, top_probs), start=1):
    top_k_rows.append({
        "rank": rank,
        "candidate_token": vocab[int(idx)],
        "logit": round(float(logits[idx]), 4),
        "original_probability": round(float(base_probs[idx]), 4),
        "top_k_probability": round(float(adjusted_prob), 4),
    })

sample_rows = []
for seed in seeds:
    token, r = sample_from_probs(vocab, base_probs, seed)
    sample_rows.append({
        "seed": seed,
        "random_value": round(r, 4),
        "sampled_token": token,
        "note": "同じ確率でも乱数が違うと選ばれるtokenが変わる",
    })

score_df = pd.DataFrame(score_rows)
temperature_df = pd.DataFrame(temperature_rows)
top_k_df = pd.DataFrame(top_k_rows)
sample_df = pd.DataFrame(sample_rows)
summary_df = pd.DataFrame([
    {"mode": "greedy", "selected_token": greedy_token, "rule": "probabilityが最大のtokenを選ぶ"},
    {"mode": "sampling", "selected_token": sample_df.loc[0, "sampled_token"], "rule": "probabilityに沿って乱数で選ぶ"},
    {"mode": "top_k", "selected_token": top_k_df.loc[0, "candidate_token"], "rule": f"上位{top_k}件だけに絞って選ぶ"},
])

# Python in Excelで最後に表示したい表を選びます。
result_df = score_df
# result_df = temperature_df
# result_df = top_k_df
# result_df = sample_df
# result_df = summary_df

result_df
