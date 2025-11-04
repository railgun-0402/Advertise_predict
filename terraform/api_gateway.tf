# API本体
resource "aws_api_gateway_rest_api" "cm_api" {
  name        = "cm-predict-api"
  description = "API for CM prediction demo"
}

# ルートに対してPOSTを許可
resource "aws_api_gateway_resource" "root_resource" {
  rest_api_id = aws_api_gateway_rest_api.cm_api.id
  parent_id   = aws_api_gateway_rest_api.cm_api.root_resource_id
  path_part   = "predict"
}

resource "aws_api_gateway_method" "post_predict" {
  rest_api_id   = aws_api_gateway_rest_api.cm_api.id
  resource_id   = aws_api_gateway_resource.root_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

# Lambda統合
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.cm_api.id
  resource_id = aws_api_gateway_resource.root_resource.id
  http_method = aws_api_gateway_method.post_predict.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cm_predict.invoke_arn
}

# デプロイ用
resource "aws_api_gateway_deployment" "cm_api_deploy" {
  depends_on = [aws_api_gateway_integration.lambda_integration]

  rest_api_id = aws_api_gateway_rest_api.cm_api.id
  stage_name  = "dev"
}

# API Gateway から Lambda を呼べるように
resource "aws_lambda_permission" "apigw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cm_predict.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.cm_api.execution_arn}/*/*"
}

output "invoke_url" {
  value = "${aws_api_gateway_deployment.cm_api_deploy.invoke_url}predict"
}
