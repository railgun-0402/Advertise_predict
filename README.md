# Advertise_predict

## 🎯 概要
- 広告の効果（ROI・視聴数）をAIで予測するPoC
- 自然文による問い合わせを受け取り、Bedrockエージェントが構造化 → SageMakerの予測モデルを呼び出し → 結果を説明文で返す流れを構築予定

## 🧩 使用技術
| レイヤー         | サービス                          | 役割                             |
| ------------ | ----------------------------- | ------------------------------ |
| API層         | **API Gateway**               | HTTPリクエストを受けてLambdaに転送         |
| ロジック層        | **Lambda (Python)**           | 入力をBedrock Agentに渡す・レスポンスを返却   |
| AIオーケストレーション | **Bedrock Agent (Claude 3系)** | ユーザー自然文を解釈し、SageMakerツールを呼び出す  |
| 予測モデル層       | **SageMaker Endpoint**        | ROIを数値で予測（PoCでは固定値でもOK）        |
| IaC          | **Terraform**                 | API Gateway, Lambda, IAM構成を自動化 |

## 🚀 セットアップ手順
- AWS CLI / Terraform / Python3.12 がローカルにインストール
- IAM権限:
  - lambda:*, apigateway:*, sagemaker:*, bedrock:*, iam:*
