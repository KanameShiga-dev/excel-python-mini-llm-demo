# Excelで体験する言語モデルのしくみ 第9回: Backpropagation

Excel for Microsoft 365 の Python in Excelで、出力側のgradientを前段の重みや入力へ戻すBackpropagationを小さく体験する教材です。

## この回で学べること

- `dLoss/dlogit = probability - target` が第8回のLossとつながっていること
- `dLoss/dW = outer(x, dlogit)` として重みごとの修正量を作れること
- `dLoss/dx = dlogit @ W.T` が前段へ戻る信号になること
- 1ステップ更新後に正解確率が上がり、Lossが下がること
- 第10回RAGへ、学習そのものではなく外部資料をつなぐ話が接続すること

## ファイル

| ファイル | 内容 |
|---|---|
| `excel_backpropagation_demo.xlsx` | デモ用Excel |
| `excel_backpropagation_slides.pptx` | 解説スライド |
| `excel_backpropagation_demo_code.py` | Python in Excelへ貼り付けるコード |
| `excel_backpropagation_demo_design.md` | Excelデモ設計 |
| `work/outline.md` | スライド構成 |
| `work/slides.html` | スライド制作中間HTML |
| `work/theme.css` | スライド制作中間CSS |
| `qa_report.md` | 品質確認結果 |

## 操作手順

1. `excel_backpropagation_demo.xlsx` を開きます。
2. `00_README` で今回の目的と注意を確認します。
3. `01_INPUT` で入力ベクトル、重み、bias、正解token、learning_rateを確認します。
4. `02_FORWARD_LOSS` と `03_DLOGIT` で出力側のgradientを確認します。
5. `04_DW_DX` で重みWと入力xへ戻るgradientを確認します。
6. `05_UPDATE_CHECK` で1ステップ更新後にLossが下がることを見ます。
7. `10_RUN_PYTHON` の手順に沿って、`11_PYTHON_CODE` または `excel_backpropagation_demo_code.py` のコードをPython in Excelへ貼り付けます。
8. `Ctrl + Enter` で実行し、`result_df` の表を確認します。

## Python in Excel実行環境

教材コード自体は外部APIを呼びません。ただし Python in Excel の実行環境は Microsoft Cloud 上なので、Excel上で実行するにはインターネット接続と対応する Microsoft 365 環境が必要です。完全ローカルで再現したい場合は、`excel_backpropagation_demo_code.py` をローカルPythonで実行してください。

## 実際のLLMとの差分

- この教材は1サンプル・1線形層だけを扱います。
- 実LLMのAttention、FFN、LayerNorm、残差接続、全層Backpropagationは再現していません。
- 大量データ、ミニバッチ、Adamなどの最適化器、分散学習は扱いません。
- 実LLMのtokenizer、巨大語彙、学習済み重み、安全制御は再現していません。
- 大規模LLMそのものをExcelで再現する教材ではありません。

## 次回への接続

第10回「RAG」では、モデルの内部重みを更新する学習ではなく、外部資料を検索して回答に使う構成へ進みます。
