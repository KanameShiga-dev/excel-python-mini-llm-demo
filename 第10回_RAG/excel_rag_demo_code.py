import pandas as pd

input_source_df = xl("'01_INPUT'!A6:C9", headers=True).dropna(how="all")
documents_source_df = xl("'02_DOCUMENTS'!A5:D12", headers=True).dropna(how="all")
query_features_source_df = xl("'03_QUERY_FEATURES'!A5:C13", headers=True).dropna(how="all")

settings = dict(zip(input_source_df["parameter"].astype(str), input_source_df["value"]))
question = str(settings.get("question", ""))
top_k = int(float(settings.get("top_k", 3)))
score_threshold = float(settings.get("score_threshold", 0.18))
query_features = [
    (str(row["query_feature"]), float(row["weight"]))
    for _, row in query_features_source_df.iterrows()
]
documents = documents_source_df[["document_id", "title", "text", "tags"]].to_dict("records")
q_terms = [term for term, weight in query_features if term.lower() in question.lower()]
max_possible = sum(weight for term, weight in query_features if term in q_terms) or 1.0
query_features_df = pd.DataFrame([{"query_feature":term,"weight":weight,"status":"queryに含まれる" if term in q_terms else "検索語として待機"} for term, weight in query_features])
documents_df = pd.DataFrame(documents)
records = []
for doc in documents:
    haystack = f"{doc['title']} {doc['text']} {doc['tags']}".lower()
    matched = [(term, weight) for term, weight in query_features if term in q_terms and term.lower() in haystack]
    raw_score = sum(weight for term, weight in matched)
    records.append({"document_id":doc["document_id"],"title":doc["title"],"matched_terms":", ".join(term for term, weight in matched) or "-","raw_score":round(raw_score,4),"score":round(raw_score/max_possible,4),"text":doc["text"]})
records = sorted(records, key=lambda row: (-row["score"], row["document_id"]))
for i, row in enumerate(records, 1):
    row["rank"] = i
    row["decision"] = "use" if i <= top_k and row["score"] >= score_threshold else "skip"
retrieval_score_df = pd.DataFrame(records)[["document_id","title","matched_terms","raw_score","score","rank","decision"]]
top_context_df = pd.DataFrame([{"rank":r["rank"],"document_id":r["document_id"],"title":r["title"],"score":r["score"],"evidence_text":r["text"]} for r in records if r["decision"] == "use"])
evidence = " / ".join([f"{row.document_id}: {row.evidence_text}" for row in top_context_df.itertuples()])
answer_draft_df = pd.DataFrame([{"field":"question","value":question},{"field":"evidence","value":evidence},{"field":"answer_draft","value":"外部APIを使わない教材では、質問に近い資料をキーワード重みで検索し、検索スコア、上位文書、根拠文、回答案が対応しているかを確認します。Python in Excelで実行する場合は、コード自体はAPIを呼ばなくても実行環境にはインターネット接続とMicrosoft 365環境が必要です。"},{"field":"caution","value":"これは教材用の簡易RAGです。embedding、ベクトルDB、reranker、LLM APIによる生成は扱いません。"}])
rag_flow_df = pd.DataFrame([{"step":1,"stage":"query","meaning":"質問文から検索語を見る"},{"step":2,"stage":"retrieve","meaning":"文書ごとに一致語と重みを足す"},{"step":3,"stage":"context","meaning":"top_kとthresholdで根拠文を選ぶ"},{"step":4,"stage":"answer","meaning":"根拠文から回答案を組み立てる"}])
result_df = retrieval_score_df
# result_df = documents_df
# result_df = query_features_df
# result_df = top_context_df
# result_df = answer_draft_df
# result_df = rag_flow_df
result_df
