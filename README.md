# Excelで体験する言語モデルのしくみ

ExcelをUIとして使い、Python in Excelで言語モデルの基本部品を小さく観察する全10回シリーズです。

この教材は、GPTのような大規模LLMそのものをExcelで再現するものではありません。入力、設定、確認表をExcelで見えるようにし、計算本体は外部PythonコードをPython in Excelへ貼り付けて実行します。

## 含まれるもの

各回フォルダには、次のファイルを置いています。

- デモ用Excel `.xlsx`
- Python in Excelへ貼り付ける外部 `.py`
- 解説スライド `.pptx`
- 各回README

## 全10回

| 回 | テーマ | フォルダ |
| --- | --- | --- |
| 第1回 | n-gram | [第1回_n-gram](./第1回_n-gram) |
| 第2回 | Self-Attention | [第2回_Self-Attention](./第2回_Self-Attention) |
| 第3回 | Embedding | [第3回_Embedding](./第3回_Embedding) |
| 第4回 | Positional Encoding | [第4回_Positional_Encoding](./第4回_Positional_Encoding) |
| 第5回 | Multi-Head Attention | [第5回_Multi-Head_Attention](./第5回_Multi-Head_Attention) |
| 第6回 | Transformer Block | [第6回_Transformer_Block](./第6回_Transformer_Block) |
| 第7回 | Softmax Generation | [第7回_Softmax_Generation](./第7回_Softmax_Generation) |
| 第8回 | Loss Learning | [第8回_Loss_Learning](./第8回_Loss_Learning) |
| 第9回 | Backpropagation | [第9回_Backpropagation](./第9回_Backpropagation) |
| 第10回 | RAG | [第10回_RAG](./第10回_RAG) |

## 必要環境

- Microsoft 365 Excel
- Python in Excel が利用できる環境

## 基本的な使い方

1. 各回フォルダのExcelファイルを開きます。
2. 入力シートで、入力値や確認対象を見ます。
3. 同じフォルダの外部 `.py` ファイルを開きます。
4. Python in ExcelのPythonエディターへコードを貼り付け、`Ctrl + Enter` で実行します。
5. Excelに返る表を切り替え、入力変更による見え方の変化を確認します。

## 注意

- `.xlsx` 形式です。マクロは含めていません。
- 外部APIキーやクラウドLLMの呼び出しは使っていません。
- 各回のExcelとPythonコードは教材用に小さく作っています。
