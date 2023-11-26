import boto3
from botocore.exceptions import ClientError

import time
import logging
import os
import subprocess

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LAMBDA_FUNCTION_NAME = os.environ['LAMBDA_FUNCTION_NAME']
STACK_NAME = os.environ['STACK_NAME']

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


def stack_exists(stack_name):
    try:
        CLOUDFORMATION_CLIENT.describe_stacks(StackName=stack_name)
        return True
    except ClientError as e:
        return 'does not exist' not in str(e)

def scale_up_down(paramWithFargate):
    CLOUDFORMATION_CLIENT.update_stack(
        StackName=STACK_NAME,
        UsePreviousTemplate=True,
        Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
        Parameters=[
            {
                'ParameterKey': 'paramDomainName',
                'UsePreviousValue': True
            },
            {
                'ParameterKey': 'paramHostedZoneId',
                'UsePreviousValue': True
            },
            {
                'ParameterKey': 'paramWithFargate',
                'ParameterValue': paramWithFargate
            }
        ],
    )


    # monitor(STACK_NAME, 'CREATE_COMPLETE')
    return {'message': 'Fargate stack deployment initiated'}

def lambda_scale_up_handler(event, context):
    return scale_up_down('true')

def lambda_scale_down_handler(event, context):
    return scale_up_down('false')
