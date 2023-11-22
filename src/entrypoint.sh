#!/bin/sh

# Check if we are running in the AWS Lambda environment according to whether FUNCTION_TASK_ROOT is set.
if [ -n "$FUNCTION_TASK_ROOT" ]; then
  # Start the Lambda function handler
  exec /var/lang/bin/python -m awslambdaric $1
else
  # Start the FastAPI application using Uvicorn for Fargate
  cd /var/task
  exec uvicorn app:app --host 0.0.0.0 --port 80
fi