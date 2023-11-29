# Define the base image from the AWS base image for Python
FROM public.ecr.aws/lambda/python:3.11

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy the handler function and any other necessary files
COPY app.py .
COPY entrypoint.sh .

EXPOSE 8080

ENTRYPOINT ["/var/task/entrypoint.sh"]
# CMD [ "app.handler" ]
