import awswrangler as wr
import boto3

def lambda_handler(event, context):
    # Get the S3 bucket names from the event
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    
    output_bucket = "micro-etl-output" 
    
    input_s3_key = event['Records'][0]['s3']['object']['key']
    
    output_s3_path = f"output-parquet-files/{input_s3_key.split('/')[-1].replace('.csv', '.parquet')}"
    
    # Read CSV files from the input S3 bucket
    df = wr.s3.read_csv(f"s3://{input_bucket}/{input_s3_key}")
    
    # Convert CSV to Parquet format and write to output bucket
    wr.s3.to_parquet(df, f"s3://{output_bucket}/{output_s3_path}")
    
    client = boto3.client('glue')
    client.start_crawler(Name='microetlgluecrawler')