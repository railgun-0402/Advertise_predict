# SageMaker を試しに触る (ダミー予測エンドポイント)

- 「とりあえず SageMaker のエンドポイントを 1 本立てて、JSON を送ると`predicted_roi`っぽいものが返る」が Goal
- 最終的には
  - Bedrock Agent のツール呼び出し先にエンドポイントを登録
  - 自然文 → 構造化 → 推論までつなげる

## 前提

- AWS アカウントがある
- SageMaker が使えるリージョンを選んでいる（モデルの種類的に、us-east-1 推奨らしい）
- IAM ロールに以下の権限があること
  - `sagemaker:*`
  - `s3:*`（今回はモデルを S3 に配置する）
- ローカルで `model.tar.gz` を作成

---

## 手順

1. 推論用のシンプルコード実装
2. それを `model.tar.gz` に固めて S3 に置く
3. SageMaker に「このアーティファクトを使用してエンドポイントを作って」と伝える
4. `invoke-endpoint` で動作確認

※今回は固定の JSON を返すだけ
