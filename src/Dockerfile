# Define the base image from the AWS base image for Python
FROM public.ecr.aws/lambda/python:3.8

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy the handler function and any other necessary files
COPY app.py .
COPY entrypoint.sh .

# Inform Docker that the container is listening on port 80
EXPOSE 80

# Set the CMD to your handler location
ENTRYPOINT ["/var/task/entrypoint.sh"]
