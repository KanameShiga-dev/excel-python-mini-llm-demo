import re
import random
from collections import Counter, defaultdict

import pandas as pd


inputs_df = xl("A5:B10", headers=True)
corpus_df = xl("'02_Corpus'!A1:C21", headers=True)


def input_value(name, default):
    labels = inputs_df.iloc[:, 0].astype(str).str.strip()
    hit = inputs_df.loc[labels == name, inputs_df.columns[1]]
    if hit.empty:
        return default
    value = hit.iloc[0]
    return default if pd.isna(value) else value


def tokenize(text):
    return re.findall(r"[A-Za-z0-9_]+|[一-龥ぁ-んァ-ヶー]+|[^\s]", text)


def detokenize(words):
    text = " ".join(words)
    return re.sub(r"\s+([。、,.!?！？])", r"\1", text)


prompt = str(input_value("開始プロンプト", "")).strip()
max_words = int(float(input_value("生成単語数", 20)))
temperature = float(input_value("温度", 0.7))
seed = int(float(input_value("乱数seed", 7)))
order = int(float(input_value("モデル次数", 2)))

max_words = max(1, min(max_words, 100))
temperature = max(0.01, min(temperature, 2.0))
order = max(1, min(order, 3))
rng = random.Random(seed)

texts = corpus_df.iloc[:, 1].dropna().astype(str).str.strip()
texts = texts[texts != ""]
tokens = tokenize(" ".join(texts))

if len(tokens) <= order:
    raise ValueError("コーパスが短すぎます。02_Corpusを確認してください。")

model = defaultdict(Counter)
for i in range(len(tokens) - order):
    context = tuple(tokens[i:i + order])
    next_word = tokens[i + order]
    model[context][next_word] += 1

fallback = Counter(t for t in tokens if t not in ["。", "、"])


def rank(counter, limit=5):
    items = [(word, count) for word, count in counter.items() if str(word).strip()]
    if not items:
        items = list(fallback.items())
    if temperature <= 0.05:
        best = max(count for word, count in items)
        weights = [1 if count == best else 0 for word, count in items]
    else:
        weights = [count ** (1.0 / temperature) for word, count in items]
    total = sum(weights) or 1
    ranked = []
    for (word, count), weight in zip(items, weights):
        ranked.append((word, count, weight / total))
    ranked.sort(key=lambda row: row[2], reverse=True)
    return ranked[:limit]


def sample(counter):
    ranked = rank(counter, 1000)
    threshold = rng.random()
    acc = 0
    for word, count, probability in ranked:
        acc += probability
        if threshold <= acc:
            return word
    return ranked[-1][0]


generated = tokenize(prompt)
if not generated:
    generated = tokens[:order]
while len(generated) < order:
    generated.insert(0, tokens[0])

rows = []
for step in range(max_words):
    context = tuple(generated[-order:])
    counter = model.get(context, fallback)
    ranked = rank(counter, 5)
    next_word = sample(counter)

    if generated[-1:] == [next_word] and next_word in ["。", "、"]:
        alt = Counter()
        for word, count in counter.items():
            if word != next_word:
                alt[word] = count
        if alt:
            ranked = rank(alt, 5)
            next_word = sample(alt)

    generated.append(next_word)
    top_candidates = ", ".join(
        [
            str(word) + ":" + str(count) + "回/" + format(probability, ".0%")
            for word, count, probability in ranked
        ]
    )
    rows.append(
        {
            "generated_text": detokenize(generated) if step == 0 else "",
            "step": step + 1,
            "context": detokenize(context),
            "top_candidates": top_candidates,
            "selected": next_word,
            "generated_so_far": detokenize(generated),
        }
    )

out = pd.DataFrame(rows)
out
