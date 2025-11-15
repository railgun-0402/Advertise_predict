## 概要

- 広告がどの程度再生されるか、人気が出るかを AI に予測させてみたい
- LLM などに視聴数など数値予測してその回答を受け取れば、とりあえずのものはできるが精度が疑問
- そこで本リポジトリでは、練習として以下の実装と構築を試してみる
  - LLM に数値予測系をやらせて、その回答を使用する
  - LLM と予測 API を分け、時系列モデル等で役割を分ける

※尚、時系列モデルなり XGBoost なりの予測系ツールは未使用なので詳細は別途検討

## LLM と予測 API の構成

- そもそも LLM は文章の理解や説明に強いモデル
- なので表形式の ML の方が数値予測の精度は良い傾向にあるらしい(AI に聞いただけだが・・・)
- 広告は実際のデータが public に公開されてるかもわからんので、何かの API を使うか public データを使うか Mock にするかは要検討

### AWS 版での形

予測するためのモデルについて試しに SageMaker を使ってみる

- API Gateway
- Lambda(Python が安定かな？)
- Bedrock
- SageMaker Endpoint
- RDS/DynamoDB

### 流れ

API リクエスト
→ Lambda/API Gateway
→ Bedrock
→ SageMaker
→ 数値を Bedrock に返却
→ 説明してレスポンスとして返却

### Azure の場合

- Functions / App Service
- Azure AI Foundry：chat flow
- Azure AI Search
- Azure ML のオンラインエンドポイント or Functions
