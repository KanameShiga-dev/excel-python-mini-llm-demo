# Excelで体験する言語モデルのしくみ 第4回: Positional Encoding

このフォルダは、「Excelで体験する言語モデルのしくみ」第4回 Positional Encoding の資料置き場です。

## この回で学べること

- Embeddingだけでは単語の位置情報が足りないこと。
- Positional Encodingがpositionごとのベクトルであること。
- Transformerへの入力が `Embedding + Positional Encoding` になること。
- 同じ単語でも、位置が変わると最終ベクトルが変わること。

## ファイル

| ファイル | 内容 |
|---|---|
| `excel_positional_encoding_demo.xlsx` | デモ用Excel |
| `excel_positional_encoding_demo_code.py` | Python in Excelへ貼り付けるコード |
| `excel_positional_encoding_demo_design.md` | デモ用Excelの設計書 |
| `excel_positional_encoding_slides.pptx` | 解説スライド |
| `excel_positional_encoding_narration.md` | スライド別読み上げ原稿 |
| `series_roadmap.md` | 全10回ロードマップ |
| `youtube_description.md` | YouTube概要欄ドラフト |
| `x_post.txt` | X投稿文ドラフト |
| `screenshots/` | 確認用スクリーンショット |

## 使い方

1. `excel_positional_encoding_demo.xlsx` を開きます。
2. `00_README` で今回の目的を確認します。
3. `01_INPUT` で文Aと文Bのtokenとpositionを確認します。
4. `02_EMBEDDING` で単語ごとのEmbeddingを確認します。
5. `03_POSITIONAL_ENCODING` でpositionごとの位置ベクトルを確認します。
6. `04_ADD_RESULT` で `Embedding + Positional Encoding` の結果を確認します。
7. `05_COMPARE` で同じ単語が別の位置にある場合を比較します。
8. 必要に応じて `10_RUN_PYTHON` の手順に沿って、外部ファイル `excel_positional_encoding_demo_code.py` からPython in Excelへ貼り付けて実行します。

## Pythonコードの扱い

このシリーズでは、Excelシート内にある長いコードをコピーする運用は推奨しません。

Python in Excelへ貼り付けるコードは、必ず外部ファイル `excel_positional_encoding_demo_code.py` を正として使います。
`11_PYTHON_CODE` シートは、コード本文ではなく、この運用を確認するための案内シートです。

## 一番大事なポイント

同じ単語でも、位置が変わるとTransformerに渡される最終ベクトルが変わります。

たとえば「私」という単語は、文Aではposition 0、文Bではposition 2にあります。
Embeddingとしての「私」は同じですが、足されるPositional Encodingが違うため、最終ベクトルは違います。

## 注意

このExcelでは、教材用に分かりやすい小さなEmbeddingを使っています。
本物の大規模LLMでは、もっと多くの次元を使い、Embeddingや位置表現の扱いもより複雑です。

この回では、数式を暗記することではなく、単語の意味に位置情報を足すという考え方を理解することを目的にします。
