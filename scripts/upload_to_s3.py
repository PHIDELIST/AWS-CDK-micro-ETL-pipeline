import boto3

def upload_file_to_s3(file_path, bucket_name, object_name):
    """
    Uploads a file to an S3 bucket.

    :param file_path: Path to the file to upload.
    :param bucket_name: Name of the S3 bucket.
    :param object_name: S3 object key.
    :return: True if file was uploaded successfully, else False.
    """

    s3_client = boto3.client('s3')

    try:
        
        s3_client.upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        print(f"Failed to upload file '{file_path}' to S3 bucket '{bucket_name}' with object key '{object_name}': {e}")
        return False
    else:
        print(f"File '{file_path}' uploaded successfully to S3 bucket '{bucket_name}' with object key '{object_name}'")
        return True

# path to file you want to upload
file_path = 'sample-data/data.json' 
bucket_name = 'micro-etl-input'
object_name = 'data1.json'

upload_file_to_s3(file_path, bucket_name, object_name)
