# Excelで体験する言語モデルのしくみ 第7回: Softmaxと生成のばらつき

Excel for Microsoft 365 の Python in Excelで、Softmaxと次token選択のばらつきを小さく体験する教材です。

## この回で学べること

- logitは確率そのものではなく、Softmaxで確率に変換すること
- temperatureで確率分布の尖り方が変わること
- greedyとsamplingで次tokenの選び方が違うこと
- seed違いでsampling結果がばらつくこと
- 第8回のLossと学習へ、確率と正解の差がつながること

## ファイル

| ファイル | 内容 |
|---|---|
| `excel_softmax_generation_demo.xlsx` | デモ用Excel |
| `excel_softmax_generation_slides.pptx` | 解説スライド |
| `excel_softmax_generation_demo_code.py` | Python in Excelへ貼り付けるコード |
| `excel_softmax_generation_demo_design.md` | Excelデモ設計 |
| `work/outline.md` | スライド構成 |
| `work/slides.html` | スライド制作中間HTML |
| `work/theme.css` | スライド制作中間CSS |
| `qa_report.md` | 品質確認結果 |

## 操作手順

1. `excel_softmax_generation_demo.xlsx` を開きます。
2. `00_README` で今回の目的と注意を確認します。
3. `01_INPUT` で候補token、logit、temperature、top_k、seedを確認します。
4. `02_LOGITS_SOFTMAX` と `03_TEMPERATURE` で確率表を確認します。
5. `04_SELECTION_METHODS` と `05_SAMPLING_RUNS` で選択方法の違いを見ます。
6. `10_RUN_PYTHON` の手順に沿って、`11_PYTHON_CODE` または `excel_softmax_generation_demo_code.py` のコードをPython in Excelへ貼り付けます。
7. `Ctrl + Enter` で実行し、`result_df` の表を確認します。

## 実際のLLMとの差分

- この教材は6候補だけの小さな語彙を扱います。
- logitは教材用の固定値で、実際のモデル計算から得たものではありません。
- top-p、beam search、repetition penalty、stop条件などの実装差は扱いません。
- 実LLMのトークナイザー、巨大語彙、文脈更新、安全制御は再現していません。
- 大規模LLMそのものをExcelで再現する教材ではありません。

## 次回への接続

第8回「Lossと学習」では、今回作った確率表と正解tokenのズレをLossとして数値化し、学習の入口へ進みます。
