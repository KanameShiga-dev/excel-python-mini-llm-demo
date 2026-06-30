# Excelで体験する言語モデルのしくみ 第8回: Lossと学習

Excel for Microsoft 365 の Python in Excelで、正解tokenとのズレをLossとして数値化し、簡略的な1ステップ更新でLossが下がる様子を体験する教材です。

## この回で学べること

- 正解tokenの確率が低いほどCross Entropy Lossが大きくなること
- `target` と `one_hot` がLoss計算の基準になること
- `gradient = probability - target` がlogitを動かす方向になること
- 1ステップ更新後に正解確率が上がり、Lossが下がること
- 第9回Backpropagationへ、Lossの信号を前へ戻す話がつながること

## ファイル

| ファイル | 内容 |
|---|---|
| `excel_loss_learning_demo.xlsx` | デモ用Excel |
| `excel_loss_learning_slides.pptx` | 解説スライド |
| `excel_loss_learning_demo_code.py` | Python in Excelへ貼り付けるコード |
| `excel_loss_learning_demo_design.md` | Excelデモ設計 |
| `work/outline.md` | スライド構成 |
| `work/slides.html` | スライド制作中間HTML |
| `work/theme.css` | スライド制作中間CSS |
| `qa_report.md` | 品質確認結果 |

## 操作手順

1. `excel_loss_learning_demo.xlsx` を開きます。
2. `00_README` で今回の目的と注意を確認します。
3. `01_INPUT` で候補token、初期logit、正解token、learning_rateを確認します。
4. `02_PROB_LOSS` で正解tokenの確率とLossを確認します。
5. `03_TARGET_GRADIENT` と `04_LEARNING_STEP` で更新方向と更新後の変化を見ます。
6. `10_RUN_PYTHON` の手順に沿って、`11_PYTHON_CODE` または `excel_loss_learning_demo_code.py` のコードをPython in Excelへ貼り付けます。
7. `Ctrl + Enter` で実行し、`result_df` の表を確認します。

## Python in Excel実行環境

教材コード自体は外部APIを呼びません。ただし Python in Excel の実行環境は Microsoft Cloud 上なので、Excel上で実行するにはインターネット接続と対応する Microsoft 365 環境が必要です。完全ローカルで再現したい場合は、`excel_loss_learning_demo_code.py` をローカルPythonで実行してください。

## 実際のLLMとの差分

- この教材は6候補だけの小さな語彙を扱います。
- 実際のモデル重みではなく、教材用にlogitを直接更新します。
- 大量データ、ミニバッチ、Adamなどの最適化器、分散学習は扱いません。
- 実LLMのtokenizer、巨大語彙、学習済み重み、安全制御は再現していません。
- 大規模LLMそのものをExcelで再現する教材ではありません。

## 次回への接続

第9回「Backpropagation」では、今回のLossとgradientを、logitより前の重みへどう戻していくかを扱います。
