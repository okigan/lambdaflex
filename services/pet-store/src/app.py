import logging
import os
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function........')


app = FastAPI(
    # root_path='/prod' if 'LAMBDA_TASK_ROOT' in os.environ else '/' 
)

mangum_handler = Mangum(app)

def handler(event, context):
    logger.info('Handling event: %s', event)
    logger.info('Handling context: %s', context)

    result = mangum_handler(event, context)

    logger.info('Handling result: %s', result)

    return result


@app.get("/")
def get_root():
    return {"Hello": "World"}

STACK_NAME = os.environ.get('STACK_NAME', 'STACK_NAME_IS_NOT_DEFINED')

CLOUDFORMATION_CLIENT = boto3.client('cloudformation')

@app.get("/stack-status")
def get_stack_status():
    logger.info('Starting get_stack_status')
    logger.info(f'Stack name: {STACK_NAME}')

    stacks = CLOUDFORMATION_CLIENT.describe_stacks(StackName=STACK_NAME)
    status = stacks['Stacks'][0]['StackStatus']
    logger.info(f'Stack status: {status}')

    return {"status": status}


class Pet(BaseModel):
    id: int
    name: str
    category: str
    price: float

# Dummy data
pets_db = [
    Pet(id=1, name="Dog", category="Mammal", price=500.0),
    Pet(id=2, name="Cat", category="Mammal", price=300.0),
    Pet(id=3, name="Parrot", category="Bird", price=150.0),
]

@app.get("/pets", response_model=List[Pet])
async def get_pets():
    return pets_db

@app.get("/pets/{pet_id}", response_model=Pet)
async def get_pet(pet_id: int):
    pet = next((p for p in pets_db if p.id == pet_id), None)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@app.post("/pets", response_model=Pet)
async def create_pet(pet: Pet):
    pets_db.append(pet)
    return pet

@app.put("/pets/{pet_id}", response_model=Pet)
async def update_pet(pet_id: int, updated_pet: Pet):
    pet = next((p for p in pets_db if p.id == pet_id), None)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    pet.name = updated_pet.name
    pet.category = updated_pet.category
    pet.price = updated_pet.price
    return pet

if __name__ == "__main__":
    logger.info('processing __main__ condition')
    # if 'LAMBDA_TASK_ROOT' not in os.environ:
    logger.info('LAMBDA_TASK_ROOT in os.environ')
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

logger.info('Loading function complete')
