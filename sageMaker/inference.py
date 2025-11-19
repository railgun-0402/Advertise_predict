# inference.py
import json
import joblib
import os

def model_fn(model_dir):
    """
    SageMaker がコンテナ起動時に呼ぶ。
    ここで学習済みモデルを読み込んで返す。
    model_dir は /opt/ml/model が渡ってくる想定。
    """
    model_path = os.path.join(model_dir, "model.joblib")
    model = joblib.load(model_path)
    return model

def input_fn(request_body, content_type):
    """
    エンドポイントに届いたリクエストボディを Python オブジェクトに変換。
    今回は JSON 前提で "spots" を取り出す例にしています。
    """
    data = json.loads(request_body)

    # 万人向けに message/value も受け取れるようにしておくならこんな感じでもOK
    # 今回は「学習モデルに渡す値」として spots を使う想定。
    spots = data.get("spots")
    if spots is None:
        # spots がない時はダミー値 or エラーにしても良い
        raise ValueError("spots が指定されていません")

    return float(spots)

def predict_fn(input_data, model):
    """
    input_fn の戻り値 (spots) と model を受け取り、モデルで推論を実行。
    """
    # input_data は単一の float を想定
    pred = model.predict([[input_data]])[0]
    return {
        "predicted_roi": float(pred),
        "input_spots": input_data
    }

def output_fn(prediction, accept):
    """
    レスポンスとして返す JSON 文字列を生成。
    """
    return json.dumps(prediction)
