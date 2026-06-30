# Excelで体験する言語モデルのしくみ 第10回: RAG

Excel for Microsoft 365 の Python in Excelで、外部資料を検索し、根拠文を使って回答案を作るRAGの小さな流れを体験する教材です。

## この回で学べること

- RAGはモデルの重みを更新するのではなく、外部資料を検索して回答に使う構成であること
- 質問、検索スコア、上位文書、根拠文、回答案を分けて確認すること
- 第1回から第9回で見た内部計算と、第10回の外部参照の違い
- 教材用RAGと実サービスのRAGの差分

## ファイル

| ファイル | 内容 |
|---|---|
| `excel_rag_demo.xlsx` | デモ用Excel |
| `excel_rag_slides.pptx` | 解説スライド |
| `excel_rag_demo_code.py` | Python in Excelへ貼り付けるコード |
| `excel_rag_demo_design.md` | Excelデモ設計 |
| `work/outline.md` | スライド構成 |
| `work/slides.html` | スライド制作中間HTML |
| `work/theme.css` | スライド制作中間CSS |
| `qa_report.md` | 品質確認結果 |

## 操作手順

1. `excel_rag_demo.xlsx` を開きます。
2. `00_README` で今回の目的と注意を確認します。
3. `01_INPUT` で質問文、`top_k`、`score_threshold` を確認します。
4. `02_DOCUMENTS` で検索対象の小さな資料表を確認します。
5. `04_RETRIEVAL_SCORE` でどの文書が根拠候補になったかを確認します。
6. `05_TOP_CONTEXT` と `06_ANSWER_DRAFT` で根拠文と回答案の対応を見ます。
7. `10_RUN_PYTHON` の手順に沿って、`11_PYTHON_CODE` または `excel_rag_demo_code.py` のコードをPython in Excelへ貼り付けます。
8. `Ctrl + Enter` で実行し、`result_df` の表を確認します。

## Python in Excel実行環境

教材コード自体は外部APIを呼びません。ただし Python in Excel の実行環境は Microsoft Cloud 上なので、Excel上で実行するにはインターネット接続と対応する Microsoft 365 環境が必要です。完全ローカルで再現したい場合は、`excel_rag_demo_code.py` をローカルPythonで実行してください。

## 実際のRAGとの差分

- この教材はキーワード重みによる簡易検索です。embedding検索やベクトルDBは再現していません。
- chunking、reranker、プロンプト設計、権限管理、監査ログは扱いません。
- 回答生成はLLM APIではなく、検索結果から回答テンプレートを組み立てます。
- 実サービスのRAG基盤では、更新頻度、アクセス制御、出典表示、評価、セキュリティ設計が必要です。

## シリーズの締め

第1回から第9回では、token、Attention、Softmax、Loss、Backpropagationのようなモデル内部の計算を小さく見ました。第10回では、学習済みモデルの外側に外部資料をつなぎ、根拠を使って答える構成へ視点を広げます。
