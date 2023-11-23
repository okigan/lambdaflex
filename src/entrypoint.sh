#!/bin/sh

# set

# Check if we are running in the AWS Lambda environment according to whether FUNCTION_TASK_ROOT is set.
if [ -n "$AWS_LAMBDA_FUNCTION_MEMORY_SIZE" ]; then
  echo "Running as a Lambda function"
  /var/runtime/bootstrap app.handler
else
  echo "Running as a Fargate container"
  exec uvicorn app:app --host "0.0.0.0" --port 8080 --log-level debug
fi