## AWS-CDK-MICRO-ETL-PIPELINE ARCHITECTURE
![Blank diagram (10)](https://github.com/PHIDELIST/AWS-CDK-micro-ETL-pipeline/assets/64526896/b2e2866c-ab7d-40eb-9eee-7cf61f53d582)
#### Events flow overview
When an input file in .csv or .json format is uploaded to the ‘input s3 bucket’, it trigger a Lambda function running as a docker container that reads the file into a data frame. The script uses awsdatawrangler python library to perform transformation to manipulate the data, convert the data to parquet format and writes the output paequet file to an ‘Output s3 bucket’. Then it trigers a glue crawler to update the Glue catalog with the metadata. an Athena tables are created on top of the processed s3 files to enable users to run analytical queries on the dataset. 
 
### Prerequisites
+ AWS CLI
+ VALID AWS ACCESS CREDENTIALS
+ PYTHON
+ Docker
### Deploy the solution
1. pip install requirements.txt
2. cdk bootstrap
3. cdk synth
4. cdk deploy

### Clean up
1. cdk destroy
