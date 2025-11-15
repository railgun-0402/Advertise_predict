# SageMaker を試しに触る (ダミー予測エンドポイント)

- 「とりあえず SageMaker のエンドポイントを 1 本立てて、JSON を送ると`predicted_roi`っぽいものが返る」が Goal
- 最終的には
  - Bedrock Agent のツール呼び出し先にエンドポイントを登録
  - 自然文 → 構造化 → 推論までつなげる

## SageMaker の特徴

AWS の“ML モデルをホストして推論 API として提供する”ためのサービス

- 自前モデルを API 化（エンドポイント化）
- CPU/GPU インスタンスで高速推論
- オートスケール
- モデル更新が簡単（再デプロイ）
- ログ / モニタリング統合

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

```bash
mkdir -p model
cp inference.py model/
cd model
tar -czf model.tar.gz inference.py
```

- 作成された `model.tar.gz` を S3 にアップロード

```bash
aws s3 cp model.tar.gz s3://YOUR-BUCKET-NAME/cm-demo/model.tar.gz
```

3. SageMaker に「このアーティファクトを使用してエンドポイントを作って」と伝える

- モデルの作成

```bash
aws sagemaker create-model \
  --model-name cm-roi-dummy-model \
  --primary-container Image="683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3",ModelDataUrl="s3://YOUR-BUCKET-NAME/cm-demo/model.tar.gz" \
  --execution-role-arn arn:aws:iam::YOUR_ACCOUNT_ID:role/service-role/AmazonSageMaker-ExecutionRole-XXXX
```

4. エンドポイントコンフィグとエンドポイント作成

- endpoint config の作成

```bash
aws sagemaker create-endpoint-config \
  --region us-east-1 \
  --endpoint-config-name cm-roi-dummy-config \
  --production-variants VariantName=AllTraffic,ModelName=cm-roi-dummy-model,InitialInstanceCount=1,InstanceType=ml.t2.medium
```

- エンドポイントの作成

```bash
aws sagemaker create-endpoint \
  --region us-east-1 \
  --endpoint-name cm-roi-dummy-endpoint \
  --endpoint-config-name cm-roi-dummy-config
```

- エンドポイントを起動する

```bash
aws sagemaker wait endpoint-in-service \
  --region us-east-1 \
  --endpoint-name cm-roi-dummy-endpoint
```

- 実行してみる

```bash
aws sagemaker-runtime invoke-endpoint \
  --region us-east-1 \
  --endpoint-name cm-roi-dummy-endpoint \
  --body '{"region":"kanto", "spots":30, "month":"2025-11"}' \
  --content-type application/json \
  out.json
```

- 結果確認

```bash
cat out.json
```

レスポンス例：

```json
{
  "predicted_roi": 0.23,
  "received": {
    "region": "kanto",
    "spots": 30,
    "month": "2025-11"
  }
}
```

- 起動時間で課金されるので不要な時は削除！

```bash
aws sagemaker delete-endpoint \
  --region us-east-1 \
  --endpoint-name cm-roi-dummy-endpoint

aws sagemaker delete-endpoint-config \
  --region us-east-1 \
  --endpoint-config-name cm-roi-dummy-config

# 必要に応じてModelも削除
aws sagemaker delete-model \
  --region us-east-1 \
  --model-name cm-roi-dummy-model
```
