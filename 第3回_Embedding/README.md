# Excelで体験する言語モデルのしくみ 第3回: Embedding

このフォルダは、「Excelで体験する言語モデルのしくみ」第3回 Embedding の資料置き場です。

## この回で学べること

- token IDはただの番号であり、意味の近さを表すものではないこと。
- Embeddingは、tokenを複数の数値で表したベクトルであること。
- 似ているtokenは、Embeddingベクトルも近くなること。
- コサイン類似度で、token同士の近さを数値として見られること。

## ファイル

| ファイル | 内容 |
|---|---|
| `excel_embedding_demo.xlsx` | デモ用Excel |
| `excel_embedding_demo_code.py` | Python in Excelへ貼り付けるコード |
| `excel_embedding_demo_design.md` | デモ用Excelの設計書 |
| `series_roadmap.md` | 全10回ロードマップ |
| `screenshots/` | 確認用スクリーンショット |

## 使い方

1. `excel_embedding_demo.xlsx` を開きます。
2. `01_INPUT` シートで、比較したいtokenを2つ選びます。
3. 表示モードを選びます。
4. `10_RUN_PYTHON` シートの手順に沿って、Python in Excelを実行します。
5. token ID、Embedding表、ベクトル比較、類似度行列、簡易マップを確認します。

## おすすめの比較

| token A | token B | 見るポイント |
|---|---|---|
| 犬 | 猫 | 同じ動物なので近い |
| 車 | 電車 | 同じ乗り物なので近い |
| 保存 | 削除 | どちらも操作なので近い |
| DB | ファイル | どちらもシステム寄りなので近い |
| 犬 | DB | 分類が違うので遠い |

## 注意

このExcelでは、教材用に分かりやすい小さなEmbeddingを使っています。
本物の大規模LLMでは、もっと多くの次元を使い、Embeddingの値は学習によって調整されます。

この回では、Embeddingの学習方法までは扱いません。
学習によって値が変わる話は、第8回 Lossと学習、第9回 Backpropagation につなげます。
