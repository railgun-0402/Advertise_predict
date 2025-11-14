import json

# SageMakerのスクリプトモードでは、`inference.py` に `model_fn`, `input_fn`, `predict_fn`, `output_fn` を書いておくとそれを使って推論できるらしい

# 何を使って推論するかをロードする
def model_fn(model_dir):
    # 学習済みモデル実装時に追加
    return None

# リクエストをPythonオブジェクト変換
def input_fn(request_body, content_type):
    # 本来はAPI GatewayとかBedrockからJSONを取得する
    if content_type == "application/json":
        return json.loads(request_body)
    return request_body

# 予測を実行する
def predict_fn(input_data, model):
    # 本当ならここでXGBoostなどを使う
    # 今回はダミーで固定値を返す
    return {
        "predicted_roi": 0.25,
        "received": input_data
    }

# 結果をHTTPレスポンスように整形する
def output_fn(prediction, accept):
    return json.dumps(prediction)
