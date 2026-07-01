import pandas as pd
import numpy as np

input_source_df = xl("'01_INPUT'!A6:F9", headers=True).dropna(how="all")
settings_source_df = xl("'01_INPUT'!A13:C16", headers=True).dropna(how="all")

features = input_source_df["input_feature"].astype(str).tolist()
x = input_source_df["x_value"].astype(float).to_numpy()
weight_columns = [c for c in input_source_df.columns if str(c).startswith("W_to_")]
vocab = [str(c).replace("W_to_", "") for c in weight_columns]
W = input_source_df[weight_columns].astype(float).to_numpy()
settings = dict(zip(settings_source_df["parameter"].astype(str), settings_source_df["value"]))
b = np.array([float(v.strip()) for v in str(settings.get("bias", "[0.1, 0.0, -0.05, 0.08]")).strip("[]").split(",")], dtype=float)
target_token = str(settings.get("target_token", "ました"))
learning_rate = float(settings.get("learning_rate", 0.7))

def softmax(values):
    shifted = values - values.max()
    exps = np.exp(shifted)
    return exps / exps.sum()

target_index = vocab.index(target_token)
logits = x @ W + b
probabilities = softmax(logits)
one_hot = np.zeros(len(vocab))
one_hot[target_index] = 1.0
loss = -np.log(probabilities[target_index])

dlogit = probabilities - one_hot
dW = np.outer(x, dlogit)
db = dlogit.copy()
dx = dlogit @ W.T

updated_W = W - learning_rate * dW
updated_b = b - learning_rate * db
updated_logits = x @ updated_W + updated_b
updated_probabilities = softmax(updated_logits)
updated_loss = -np.log(updated_probabilities[target_index])

forward_df = pd.DataFrame({
    "candidate_token": vocab,
    "logit_before": np.round(logits, 4),
    "probability_before": np.round(probabilities, 4),
    "is_target": one_hot.astype(int),
    "dLoss_dlogit": np.round(dlogit, 4),
})

dW_df = pd.DataFrame(dW, columns=[f"dW_to_{token}" for token in vocab])
dW_df.insert(0, "input_feature", features)
dW_df.iloc[:, 1:] = dW_df.iloc[:, 1:].round(4)

dx_df = pd.DataFrame({
    "input_feature": features,
    "x_value": x,
    "dLoss_dx": np.round(dx, 4),
})

update_df = pd.DataFrame({
    "candidate_token": vocab,
    "logit_before": np.round(logits, 4),
    "probability_before": np.round(probabilities, 4),
    "logit_after": np.round(updated_logits, 4),
    "probability_after": np.round(updated_probabilities, 4),
    "probability_change": np.round(updated_probabilities - probabilities, 4),
})

summary_df = pd.DataFrame([
    {"state": "before", "target_token": target_token, "target_probability": round(float(probabilities[target_index]), 4), "loss": round(float(loss), 4)},
    {"state": "after one step", "target_token": target_token, "target_probability": round(float(updated_probabilities[target_index]), 4), "loss": round(float(updated_loss), 4)},
])

chain_rule_df = pd.DataFrame([
    {"step": 1, "gradient": "dLoss/dlogit", "formula": "probability - target", "meaning": "出力側のズレ"},
    {"step": 2, "gradient": "dLoss/dW", "formula": "x outer dlogit", "meaning": "重みごとの責任"},
    {"step": 3, "gradient": "dLoss/db", "formula": "dlogit", "meaning": "biasの責任"},
    {"step": 4, "gradient": "dLoss/dx", "formula": "dlogit @ W.T", "meaning": "前段へ戻る信号"},
    {"step": 5, "gradient": "update", "formula": "W - lr * dW", "meaning": "Lossを下げる向き"},
])

# Python in Excelで最後に表示したい表を選びます。
result_df = forward_df
# result_df = dW_df
# result_df = dx_df
# result_df = update_df
# result_df = summary_df
# result_df = chain_rule_df

result_df
