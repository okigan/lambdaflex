import logging
from fastapi import FastAPI
from mangum import Mangum

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')


app = FastAPI()

@app.get("/asf")
def read_root():
    return {"Hello": "World"}

handler = Mangum(app)

logger.info('Loading function complete')


