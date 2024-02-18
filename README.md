## AWS-CDK-MICRO-ETL-PIPELINE ARCHITECTURE
![Blank diagram (1)](https://github.com/PHIDELIST/AWS-CDK-micro-ETL-pipeline/assets/64526896/0e66f4cf-93d1-4510-8768-320b5dd68a9e)

#### Events flow overview
When an input file in .csv or .json format is uploaded to the ‘input s3 bucket’, it trigger a Lambda function running as a docker container that reads the file into a data frame. The script uses awsdatawrangler python library to perform transformation to manipulate the data, convert the data to parquet format and writes the output paequet file to an ‘Output s3 bucket’. Then it trigers a glue crawler to update the Glue catalog with the metadata. an Athena tables are created on top of the processed s3 files to enable users to run analytical queries on the dataset. 
 
### Prerequisites
+ AWS CLI
+ VALID AWS ACCESS CREDENTIALS
+ PYTHON
+ Docker
### Deploy the solution
1. Clone the project repository.
2. Navigate to the project directory.
3. pip install requirements.txt
4. cdk bootstrap
5. cdk synth
6. cdk deploy

### Usage
1. use `python scripts/upload_to_s3.py` to upload your raw data to input s3 bucket.
2. Wait for around 2 minutes
3. use `python scripts/run_athena_query.py` to query your processed data in output s3 bucket through Athena. feel free to modify the sql query in `run_athena_query.py` to suite your needs.

### Clean up
This will remove all resources created by this project from you AWS account
1. cdk destroy
## License
This project is licensed under the MIT License. See the [LINCENSE](https://github.com/PHIDELIST/AWS-CDK-micro-ETL-pipeline/blob/main/LINCENSE.md) file for details.
