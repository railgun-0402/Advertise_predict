# Advertise_predict

## 🎯 概要

- 広告の効果（ROI・視聴数）を AI で予測する PoC
- 自然文による問い合わせを受け取り、Bedrock エージェントが構造化 → SageMaker の予測モデルを呼び出し → 結果を説明文で返す流れを構築予定

## 🧩 使用技術

| レイヤー                | サービス                        | 役割                                               |
| ----------------------- | ------------------------------- | -------------------------------------------------- |
| API 層                  | **API Gateway**                 | HTTP リクエストを受けて Lambda に転送              |
| ロジック層              | **Lambda (Python)**             | 入力を Bedrock Agent に渡す・レスポンスを返却      |
| AI オーケストレーション | **Bedrock Agent (Claude 3 系)** | ユーザー自然文を解釈し、SageMaker ツールを呼び出す |
| 予測モデル層            | **SageMaker Endpoint**          | ROI を数値で予測（PoC では固定値でも OK）          |
| IaC                     | **Terraform**                   | API Gateway, Lambda, IAM 構成を自動化              |

## 🚀 セットアップ手順

- AWS CLI / Terraform / Python3.12 がローカルにインストール
- IAM 権限:
  - lambda:_, apigateway:_, sagemaker:_, bedrock:_, iam:\*

## Curl 例

### request

```
url -X POST https://xxx/dev/predict -d '{"query":"〜を教えて"}' -H 'Content-Type: application/json'
```

### response

```
{
  "message": "ok",
  "answer": "〜できます。"
}
```

## Docs

- [Bedrock 連携手順](docs/bedrock_integration.md)
- [SageMaker クイックスタート](docs/sagemaker_quickstart.md)
- [アーキテクチャ概要](docs/architecture.md)
