import json
import os
import boto3

BEDROCK_REGION = os.environ.get("AWS_REGION", "ap-northeast-1")
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")

bedrock = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)

def handler(event, context):
    body = {}
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError:
            body = {"raw": event["body"]}

    # TODO: ここを動的にする
    user_query = body.get("query", "CMのROI予測について簡単に説明してください")

    # Bedrockに投げるpayload作成
    prompt = f"次の問いに簡潔に日本語で答えてください。\n\n{user_query}"
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.2,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            }
        ]
    }

    # モデル呼び出し
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(payload)
    )

    # レスポンス取り出し
    resp_body = json.loads(response["body"].read())
    # Claude v3系は content の中に text が入る
    # TODO: textだけでなく、UIに合わせて必要な値を取得する
    bedrock_answer = ""
    if "content" in resp_body and len(resp_body["content"]) > 0:
        bedrock_answer = resp_body["content"][0]["text"]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "message": "ok",
            "answer": bedrock_answer
        }, ensure_ascii=False)
    }