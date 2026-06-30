# Excelで体験する言語モデルのしくみ 第5回: Multi-Head Attention

このフォルダは、「Excelで体験する言語モデルのしくみ」第5回 Multi-Head Attention の資料置き場です。

## この回で学べること

- 入力ベクトル `X` から `Q`、`K`、`V` を作る流れ。
- `score = QK^T / sqrt(d_k)` を計算する流れ。
- scoreをsoftmaxでattention weightに変える流れ。
- `attention weight @ V` でHeadごとの出力を作る流れ。
- Head 1とHead 2の出力を横に結合する流れ。

## ファイル

| ファイル | 内容 |
|---|---|
| `excel_multi_head_attention_demo.xlsx` | デモ用Excel |
| `excel_multi_head_attention_demo_code.py` | Python in Excelへ貼り付けるコード |
| `excel_multi_head_attention_demo_design.md` | デモ用Excelの設計書 |
| `excel_multi_head_attention_slides.pptx` | 解説スライド |
| `excel_multi_head_attention_narration.md` | スライド別読み上げ原稿 |
| `series_roadmap.md` | 全10回ロードマップ |
| `youtube_description.md` | YouTube概要欄ドラフト |
| `x_post.txt` | X投稿文ドラフト |
| `screenshots/` | 確認用スクリーンショット |

## 使い方

1. `excel_multi_head_attention_demo.xlsx` を開きます。
2. `00_README` で今回の目的を確認します。
3. `01_INPUT_X` で入力ベクトル `X` を確認します。
4. `02_WEIGHTS_HEAD1` から `06_OUTPUT_HEAD1` でHead 1の計算を追います。
5. `07_WEIGHTS_HEAD2` から `11_OUTPUT_HEAD2` でHead 2の計算を追います。
6. `12_CONCAT` で2つのHead出力を横に結合した結果を見ます。
7. `13_FOCUS_TRACE` で `食べる` をqueryにした計算の流れを1つの表で確認します。
8. `14_RUN_PYTHON` の手順に沿って、外部ファイル `excel_multi_head_attention_demo_code.py` をPython in Excelへ貼り付けて実行します。

## Pythonコードの扱い

Python in Excelへ貼り付けるコードは、外部ファイル `excel_multi_head_attention_demo_code.py` を正として使います。

このコードは、Python in Excelの文字数制限に収まるように短縮しています。
既定では、`python_result_df = focus_trace_df.copy()` にしてあり、`食べる` をqueryにした計算追跡を表示します。

表示したい表は、コード末尾の `python_result_df` 選択行で切り替えます。

```python
python_result_df = focus_trace_df.copy()
# python_result_df = concat_df.copy()
# python_result_df = qkv_head1_df.copy()
# python_result_df = score_head1_df.copy()
# python_result_df = softmax_head1_df.copy()
```

## 一番大事なポイント

このデモでは、Attention重みを手で貼り付けません。

教材用の `Wq`、`Wk`、`Wv` は固定パラメータとして用意しますが、そこから先の `Q`、`K`、`V`、score、softmax、output、concatはPythonで計算します。

Multi-Head Attentionでは、Headごとに別の `Wq`、`Wk`、`Wv` を使うため、同じ入力 `X` からでもHeadごとに違う出力が作られます。

## 注意

このExcelは教材用の小さなデモです。
本物の大規模LLMでは、次元数、Head数、重みの学習方法はもっと大きく複雑です。

この回では、実際の規模を再現することではなく、Multi-Head Attentionの計算手順を追えることを目的にします。
