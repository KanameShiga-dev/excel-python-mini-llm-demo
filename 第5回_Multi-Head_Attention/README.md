# 第5回 Multi-Head Attention

ExcelをUIとして使い、Python in Excelで言語モデルの仕組みを小さく確認する教材です。

複数のHeadで同じ入力を違う観点から見る流れを確認します。

## ファイル

| ファイル | 内容 |
| --- | --- |
| `excel_multi_head_attention_demo.xlsx` | デモ用Excel。入力、設定、確認表を含みます。 |
| `excel_multi_head_attention_demo_code.py` | Python in Excelへ貼り付ける外部Pythonコードです。 |
| `excel_multi_head_attention_slides.pptx` | 解説スライドです。 |
| `README.md` | この説明ファイルです。 |

## 使い方

1. `excel_multi_head_attention_demo.xlsx` を開きます。
2. Excelの入力シートで、入力値や確認対象を見ます。
3. `excel_multi_head_attention_demo_code.py` を開き、コードをPython in Excelへ貼り付けます。
4. `Ctrl + Enter` で実行します。
5. Excelに返る表を見て、入力や設定の変更で何が変わるかを確認します。

## 注意

- この教材は説明用の小さなデモです。
- GPTのような大規模LLMそのものをExcelで再現するものではありません。
- マクロ、外部APIキー、クラウドLLM呼び出しは使っていません。
