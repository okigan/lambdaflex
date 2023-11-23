#!/bin/sh

# set

# Check if we are running in the AWS Lambda environment according to whether FUNCTION_TASK_ROOT is set.
if [ -n "$AWS_LAMBDA_FUNCTION_MEMORY_SIZE" ]; then
# https://github.com/aws/aws-lambda-python-runtime-interface-client ?
  echo "Running as a Lambda function"
  export AWS_LAMBDA_LOG_LEVEL=DEBUG
  export _HANDLER=app.handler
  /var/runtime/bootstrap --help -m awslambdaric app.handler
else
  echo "Running as a Fargate container"
  exec uvicorn app:app --host "0.0.0.0" --port 8080 --log-level debug
fi