import json

def handler(event, context):
    body = {}
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError:
            body = {"raw": event["body"]}
    
    response = {
        "message": "hello from lambda",
        "input": body,
    }
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }