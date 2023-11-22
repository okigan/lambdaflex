#!/bin/bash

# Get ImageUri from Lambda function with the following name
REGION="us-east-1"
LAMBDA_FUNCTION_NAME="anyscale-dev-MyLambdaFunction-yrsZdUsDY93I"

response=$(aws lambda get-function --region ${REGION} --function-name $LAMBDA_FUNCTION_NAME)
IMAGE_URI=$(echo $response | jq -r '.Code.ImageUri')
echo "Image URI: $IMAGE_URI"

STACK_NAME="sss2"
TEMPLATE_FILE="template-fargate.yml"

aws cloudformation update-stack \
  --template-body file://$TEMPLATE_FILE \
  --stack-name $STACK_NAME \
  --region $REGION \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=ContainerImageUri,ParameterValue=$IMAGE_URI \
  --no-cli-pager \
  --disable-rollback

# Initialize last event timestamp
LAST_TIMESTAMP=""

echo "Monitoring stack events. Press Ctrl+C to stop."

# Monitor stack events in real-time
while true; do
  # Fetch stack events since the last poll
  EVENTS=$(aws cloudformation describe-stack-events \
    --stack-name $STACK_NAME \
    --region us-east-1 \
    --query "StackEvents[?Timestamp>'$LAST_TIMESTAMP'].[LogicalResourceId,ResourceStatus, ResourceType, ResourceStatusReason, Timestamp]" \
    --output table)

  # Display events if there are any
  if [ -n "$EVENTS" ]; then
    echo "$EVENTS"
  fi

  # Update last event timestamp
  LAST_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  # Fetch stack status
  STACK_STATUS=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region us-east-1 \
    --query "Stacks[0].StackStatus" \
    --output text)

  # If the stack status is a terminal state, break the loop
  if [[ "$STACK_STATUS" == "CREATE_COMPLETE" || "$STACK_STATUS" == "UPDATE_COMPLETE" || "$STACK_STATUS" == "ROLLBACK_COMPLETE" || "$STACK_STATUS" == "DELETE_COMPLETE" || "$STACK_STATUS" == "UPDATE_ROLLBACK_COMPLETE" ]]; then
    break
  fi


  # Sleep for a few seconds before checking again
  sleep 5
done
