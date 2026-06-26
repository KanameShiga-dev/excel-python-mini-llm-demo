# Excelで体験する言語モデルのしくみ

Excel for Microsoft 365 の Python セルで、言語モデルの基本にある「次の token を予測する」考え方を体験するための教材です。

これは GPT のような大規模 LLM ではありません。小さなコーパスを読み込み、直前の token から次の token を確率的に選ぶ n-gram モデルです。

## Download

- [Excelで体験する言語モデルのしくみ.xlsx](./Excelで体験する言語モデルのしくみ.xlsx)

## Requirements

- Microsoft 365 Excel
- Python in Excel が利用できる環境

## Notes

- このブックは `.xlsx` 形式です。マクロは含めていません。
- 外部 API キーやクラウド LLM の呼び出しは使っていません。
- Python セルを実行すると、`generated_text` に生成結果が表示されます。

## Demo Flow

1. `01_Demo` の入力値を確認します。
2. `03_Python_Code` のコードを Python セルに貼り付けます。
3. `Ctrl + Enter` で実行します。
4. `generated_text` と `top_candidates` を確認します。
5. `02_Corpus` や `温度`、`モデル次数` を変えて結果の違いを見ます。
