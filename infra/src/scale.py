import boto3
from botocore.exceptions import ClientError

import time
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LAMBDA_FUNCTION_NAME = os.environ.get('LAMBDA_FUNCTION_NAME', 'LAMBDA_FUNCTION_NAME_IS_NOT_DEFINED')
STACK_NAME = os.environ.get('STACK_NAME', 'STACK_NAME_IS_NOT_DEFINED')

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

def dummy_function_for_testing():
    return 'dummy_function_for_testing'


def stack_exists(stack_name):
    try:
        CLOUDFORMATION_CLIENT.describe_stacks(StackName=stack_name)
        return True
    except ClientError as e:
        return 'does not exist' not in str(e)

def scale_up_down(paramWithFargate):
    logger.info('Starting scale_up_down')

    parameters = [
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
        ]
    
    logger.info(f'paramWithFargate: {paramWithFargate}')
    logger.info(f'Stack name: {STACK_NAME}')
    logger.info(f'Parameters: {parameters}')

    result = CLOUDFORMATION_CLIENT.update_stack(
        StackName=STACK_NAME,
        UsePreviousTemplate=True,
        Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
        Parameters=parameters,
    )

    logger.info(f'Result: {result}')


    # monitor(STACK_NAME, 'CREATE_COMPLETE')
    return {'message': 'Fargate stack deployment initiated'}

def lambda_scale_up_handler(event, context):
    logger.info('Starting lambda_scale_up_handler')
    logger.info(f'Event: {event}')
    logger.info(f'Context: {context}')

    result = scale_up_down('true')

    logger.info(f'Result: {result}')

    return result

def lambda_scale_down_handler(event, context):
    logger.info('Starting lambda_scale_down_handler')
    logger.info(f'Event: {event}')
    logger.info(f'Context: {context}')

    result = scale_up_down('false')

    logger.info(f'Result: {result}')

    return result