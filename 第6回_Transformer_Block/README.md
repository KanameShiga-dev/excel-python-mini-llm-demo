# Excelで体験する言語モデルのしくみ 第6回: Transformer Block

Excel for Microsoft 365 の Python in Excelで、Transformer Blockの流れを小さく体験する教材です。

## この回で学べること

- 第5回のMulti-Head Attention出力に相当する値を受け取る流れ
- Residual connectionで元の情報を足し戻す考え方
- Layer Normalizationで値のスケールを整える考え方
- FFNでtokenごとのベクトルをさらに変換する考え方
- Block Outputが次の層や次回のSoftmaxへつながること

## ファイル

| ファイル | 内容 |
|---|---|
| `excel_transformer_block_demo.xlsx` | デモ用Excel |
| `excel_transformer_block_slides.pptx` | 解説スライド |
| `excel_transformer_block_demo_code.py` | Python in Excelへ貼り付けるコード |
| `excel_transformer_block_demo_design.md` | Excelデモ設計 |
| `work/outline.md` | スライド構成 |
| `work/slides.html` | スライド制作中間HTML |
| `work/theme.css` | スライド制作中間CSS |
| `qa_report.md` | 品質確認結果 |

## 操作手順

1. `excel_transformer_block_demo.xlsx` を開きます。
2. `00_README` で今回の目的と注意を確認します。
3. `01_INPUT` で `Input X` と `Attention Output` を確認します。
4. `02_BLOCK_FLOW` で処理順を確認します。
5. `03_ATTENTION_OUTPUT` から `07_BLOCK_OUTPUT` まで、値の変化を順に見ます。
6. `10_RUN_PYTHON` の手順に沿って、`11_PYTHON_CODE` または `excel_transformer_block_demo_code.py` のコードをPython in Excelへ貼り付けます。
7. `Ctrl + Enter` で実行し、`result_df` の表を確認します。

## 処理順

教材上の処理順は、分かりやすさを優先して次に固定しています。

`Attention Output -> Add & Norm -> FFN -> Add & Norm -> Block Output`

## 実際のTransformerやLLMとの差分

- この教材は4 token x 4次元の小さな固定値だけを扱います。
- FFNの重みは教材用に固定しており、学習は扱いません。
- Layer Normalizationは簡略モデルです。
- 実際のTransformerやLLMでは、Pre-LN、Post-LN、層数、次元数、活性化関数、正規化方式などに実装差があります。
- 大規模LLMそのものをExcelで再現する教材ではありません。

## 次回への接続

第7回「Softmaxと生成のばらつき」では、Block Outputのような次の表現から、次tokenの確率を作り、選び方によって生成がばらつくことを見ます。
