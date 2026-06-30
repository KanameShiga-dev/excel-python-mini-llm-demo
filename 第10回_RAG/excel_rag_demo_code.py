import pandas as pd

question = "Python in ExcelでRAG教材を外部APIなしで動かすとき、検索スコア、根拠、回答案の何を確認すればよいですか"
top_k = 3
score_threshold = 0.18
query_features = [('python', 1.0), ('excel', 1.0), ('rag', 1.4), ('外部api', 1.2), ('検索', 1.1), ('根拠', 1.2), ('回答', 0.9), ('教材', 0.8)]
documents = [
    {"document_id":"D01","title":"RAGの基本","text":"RAGは質問に近い外部資料を検索し、その根拠を回答に添える構成です。","tags":"rag,検索,根拠,回答"},
    {"document_id":"D02","title":"Python in Excel","text":"Python in Excelではコード実行はMicrosoft Cloud上で行われ、実行には対応するMicrosoft 365環境とインターネット接続が必要です。","tags":"python,excel,実行環境,cloud"},
    {"document_id":"D03","title":"教材用の簡略化","text":"この教材では外部APIを呼ばず、キーワード重みによる簡易スコアで検索の流れを確認します。","tags":"教材,外部api,検索,簡略化"},
    {"document_id":"D04","title":"生成の扱い","text":"回答生成はLLM APIではなく、上位文書の根拠文を使ったテンプレートで組み立てます。","tags":"回答,根拠,テンプレート,llm"},
    {"document_id":"D05","title":"前回との違い","text":"Backpropagationは内部重みを更新しますが、RAGは学習済みモデルの外側に資料をつなぎます。","tags":"backpropagation,rag,外部資料,重み"},
    {"document_id":"D06","title":"本格RAGで必要なもの","text":"実サービスではembedding、ベクトルDB、chunking、reranker、プロンプト設計、権限管理が重要です。","tags":"embedding,vector,chunking,reranker"},
    {"document_id":"D07","title":"確認する表","text":"検索スコア、上位文書、根拠文、回答案を分けて見ると、どの資料を使ったか説明しやすくなります。","tags":"検索,スコア,上位文書,根拠,回答"},
]
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
