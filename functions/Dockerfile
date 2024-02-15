# Use the official AWS Lambda base image for Python 3.8
FROM public.ecr.aws/lambda/python:3.10

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the CMD to your handler
CMD ["csv_to_parquet_lambda.lambda_handler"]
