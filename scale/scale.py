import boto3
from botocore.exceptions import ClientError

import time
import logging
import os
import subprocess

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LAMBDA_FUNCTION_NAME = os.environ['LAMBDA_FUNCTION_NAME']
STACK_NAME = 'MyFargateStack'

LAMBDA_CLIENT = boto3.client('lambda')
CLOUDFORMATION_CLIENT = boto3.client('cloudformation')



def monitor(stack_name, target_status):
    while True:
        stacks = CLOUDFORMATION_CLIENT.describe_stacks(StackName=stack_name)
        status = stacks['Stacks'][0]['StackStatus']
        logger.info(f'Stack status: {status}')

        if status == target_status or status.endswith('FAILED'):
            break
        time.sleep(5)



def lambda_scale_down_handler(event, context):
    CLOUDFORMATION_CLIENT.delete_stack(StackName=STACK_NAME)
    monitor(STACK_NAME, 'DELETE_COMPLETE')
    return {'message': 'Fargate stack deletion initiated'}



def stack_exists(stack_name):
    try:
        CLOUDFORMATION_CLIENT.describe_stacks(StackName=stack_name)
        return True
    except ClientError as e:
        return 'does not exist' not in str(e)
    

def lambda_scale_up_handler(event, context):
    subprocess.run(['ls', '-s'], check=True)

    response = LAMBDA_CLIENT.get_function(FunctionName=LAMBDA_FUNCTION_NAME)
    image_uri = response['Code']['ImageUri']
    logger.info(f'Image URI: {image_uri}')

    with open('template-fargate.yml', 'r') as template_file:
        template_body = template_file.read()

    create_or_update_stack = CLOUDFORMATION_CLIENT.create_stack if not stack_exists(STACK_NAME) else CLOUDFORMATION_CLIENT.update_stack

    create_or_update_stack(
        StackName=STACK_NAME,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
        # Include additional parameters if necessary, such as:
        Parameters=[
            {
                'ParameterKey': 'ContainerImageUri',
                'ParameterValue': image_uri
            }
        ],
    )

    monitor(STACK_NAME, 'CREATE_COMPLETE')
    return {'message': 'Fargate stack deployment initiated'}


# arn:aws:lambda:us-east-1:602375570961:function:anyscale-dev-MyLambdaFunction-UU1H8oy6y9cs
# arn:aws:lambda:us-east-1:602375570961:function:MyLambdaFunction