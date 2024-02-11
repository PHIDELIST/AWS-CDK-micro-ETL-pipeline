import awswrangler as wr
import boto3

def lambda_handler(event, context):
    # Get the S3 bucket names from the event
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    output_bucket = "micro-etl-output" 
    
    input_s3_path = event['Records'][0]['s3']['object']['key']
    
    
    output_s3_path = "output-parquet-files/"
    
    # Read CSV files from the input S3 bucket
    df = wr.s3.read_csv(f"s3://{input_bucket}/{input_s3_path}")
    
    # Convert CSV to Parquet format
    wr.s3.to_parquet(df, f"s3://{output_bucket}/{output_s3_path}")
