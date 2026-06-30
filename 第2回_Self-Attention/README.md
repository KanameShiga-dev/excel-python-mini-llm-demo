# Excelで体験する言語モデルのしくみ 第2回: Self-Attention

このフォルダは、「Excelで体験する言語モデルのしくみ」第2回 Self-Attention の資料置き場です。

## この回で学べること

- n-gramが直前の並びを見るのに対し、Self-Attentionは文全体を見られること。
- tokenごとに、どのtokenをどれくらい見るかをAttention Weightとして確認できること。
- Q、K、V、Attention Score、Attention Weight、Context Vectorの流れ。
- Attention Weightの行合計が1になり、重みつき平均としてContext Vectorが作られること。

## ファイル

| ファイル | 内容 |
|---|---|
| `excel_self_attention_demo.xlsx` | デモ用Excel |
| `excel_self_attention_demo_code.py` | Python in Excelへ貼り付けるコード |
| `excel_self_attention_demo_design.md` | デモ用Excelの設計書 |
| `excel_self_attention_slides.pptx` | 解説スライド |
| `series_roadmap.md` | 全10回ロードマップ |
| `media_assets/` | 読み上げ動画、字幕、告知文など |

## 使い方

1. `excel_self_attention_demo.xlsx` を開きます。
2. `01_INPUT` シートで入力文と表示モードを確認します。
3. `10_RUN_PYTHON` シートの手順に沿って、Python in Excelを実行します。
4. `excel_self_attention_demo_code.py` のコードをPythonエディターへ貼り付けます。
5. `Ctrl + Enter` で実行し、token、Q/K/V、Attention Weight、Context Vectorを確認します。

## 見るポイント

| 表示モード | 見ること |
|---|---|
| `token一覧` | 入力文が空白区切りtokenとしてどう扱われるか |
| `embedding` | tokenから入力ベクトルが作られる入口 |
| `Q/K/V` | 見る側、見られる側、取り出す値の3役 |
| `Attention Score` | token同士の関連スコア |
| `Attention Weight` | どのtokenをどれくらい見るか |
| `Context Vector` | Attention WeightでVを重みづけした結果 |

## 注意

このExcelは、Self-Attentionの考え方を小さな表で観察する教材です。
本物のTransformerやLLMの規模、学習済み重み、実際のtokenizerは再現していません。

第3回 Embedding では、tokenを数値ベクトルとして扱う考え方をさらに詳しく見ます。
