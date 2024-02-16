
FROM public.ecr.aws/lambda/python:3.10


COPY . ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


CMD ["csv_to_parquet_lambda.lambda_handler"]
