import logging
import os

from fastapi import FastAPI
from mangum import Mangum

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function........')


app = FastAPI(
    root_path='/prod' if 'LAMBDA_TASK_ROOT' in os.environ else '/' 
)

handler = Mangum(app)


@app.get("/asf")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    logger.info('processing __main__ condition')
    # if 'LAMBDA_TASK_ROOT' not in os.environ:
    logger.info('LAMBDA_TASK_ROOT in os.environ')
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

logger.info('Loading function complete')
