import awswrangler as wr
import boto3
import os

def lambda_handler(event, context):
    # Get the S3 bucket names from the event
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    output_bucket = "micro-etl-output" 
    input_s3_key = event['Records'][0]['s3']['object']['key']
    file_extension = os.path.splitext(input_s3_key)[-1].lower()
    output_s3_path = f"output-parquet-files/{os.path.basename(input_s3_key).replace(file_extension, '.parquet')}"

    if file_extension == '.csv':
        df = wr.s3.read_csv(f"s3://{input_bucket}/{input_s3_key}")
    elif file_extension == '.json':
        df = wr.s3.read_json(f"s3://{input_bucket}/{input_s3_key}")
    else:
        print(f"Unsupported file format: {file_extension}")
        return
    
    wr.s3.to_parquet(df, f"s3://{output_bucket}/{output_s3_path}")
    
    #Triger glue
    client = boto3.client('glue')
    response = client.start_crawler(Name='microetlgluecrawler',
                                     Targets={'S3Targets': [{'Path': f"s3://{output_bucket}/{output_s3_path}"}]})
    
    return {
        'statusCode': 200,
        'body': 'Glue crawler triggered successfully'
    }