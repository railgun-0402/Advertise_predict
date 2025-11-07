resource "aws_iam_role" "lambda_exec" {
  name = "cm-predict-lambda-exec"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Effect = "Allow"
      }
    ]
  })
}

# CloudWatch Logsへの書き込み用
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

## Call Bedrock Auth
resource "aws_iam_role_policy" "lambda_bedrock" {
    name = "lambda-bedrock-policy"
    role = aws_iam_role.lambda_exec.id

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = [
                "bedrock:InvokeModel"
            ]
            Resource = "*"
            Effect = "Allow"
        }
        ]
    })
}

resource "aws_lambda_function" "cm_predict" {
  function_name = "cm-predict-handler"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.handler"
  runtime       = "python3.12"

  filename         = "function.zip"
  source_code_hash = filebase64sha256("function.zip")

  timeout = 10
}
