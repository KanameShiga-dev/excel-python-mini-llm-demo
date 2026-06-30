import pandas as pd
import numpy as np

context_tokens = ["今日", "猫", "ごはん", "食べる"]
vocab = ["です", "ました", "ね", "よ", "犬", "走る"]
initial_logits = np.array([2.2, 1.5, 0.9, 0.4, -0.2, -0.8], dtype=float)
target_token = "ました"
learning_rate = 0.8
training_steps = 4

def softmax(values):
    shifted = values - values.max()
    exps = np.exp(shifted)
    return exps / exps.sum()

def cross_entropy(probability):
    return -np.log(probability)

target_index = vocab.index(target_token)
probabilities = softmax(initial_logits)
loss = cross_entropy(probabilities[target_index])
one_hot = np.zeros(len(vocab))
one_hot[target_index] = 1.0
gradients = probabilities - one_hot
updated_logits = initial_logits - learning_rate * gradients
updated_probabilities = softmax(updated_logits)
updated_loss = cross_entropy(updated_probabilities[target_index])

prediction_df = pd.DataFrame({
    "candidate_token": vocab,
    "logit_before": np.round(initial_logits, 4),
    "probability_before": np.round(probabilities, 4),
    "is_target": one_hot.astype(int),
    "target_loss": [round(float(loss), 4) if i == target_index else "" for i in range(len(vocab))],
})

gradient_df = pd.DataFrame({
    "candidate_token": vocab,
    "probability_before": np.round(probabilities, 4),
    "is_target": one_hot.astype(int),
    "gradient_prob_minus_target": np.round(gradients, 4),
    "logit_delta": np.round(-learning_rate * gradients, 4),
    "logit_after": np.round(updated_logits, 4),
})

learning_step_df = pd.DataFrame({
    "candidate_token": vocab,
    "logit_before": np.round(initial_logits, 4),
    "probability_before": np.round(probabilities, 4),
    "logit_after": np.round(updated_logits, 4),
    "probability_after": np.round(updated_probabilities, 4),
    "probability_change": np.round(updated_probabilities - probabilities, 4),
})

trace_rows = []
current_logits = initial_logits.copy()
for step in range(training_steps + 1):
    current_probs = softmax(current_logits)
    current_loss = cross_entropy(current_probs[target_index])
    trace_rows.append({
        "step": step,
        "target_logit": round(float(current_logits[target_index]), 4),
        "target_probability": round(float(current_probs[target_index]), 4),
        "loss": round(float(current_loss), 4),
    })
    if step < training_steps:
        current_one_hot = np.zeros(len(vocab))
        current_one_hot[target_index] = 1.0
        current_logits = current_logits - learning_rate * (current_probs - current_one_hot)

loss_trace_df = pd.DataFrame(trace_rows)
summary_df = pd.DataFrame([
    {"state": "before", "target_token": target_token, "target_probability": round(float(probabilities[target_index]), 4), "loss": round(float(loss), 4)},
    {"state": "after one step", "target_token": target_token, "target_probability": round(float(updated_probabilities[target_index]), 4), "loss": round(float(updated_loss), 4)},
])

# Python in Excelで最後に表示したい表を選びます。
result_df = prediction_df
# result_df = gradient_df
# result_df = learning_step_df
# result_df = loss_trace_df
# result_df = summary_df

result_df
