## MICRO-ETL ARCHITECTURE
![Blank diagram (10)](https://github.com/PHIDELIST/AWS-CDK-micro-ETL-pipeline/assets/64526896/b2e2866c-ab7d-40eb-9eee-7cf61f53d582)
This pattern demonstrates serverless event driven micro ETL service leveraging Data Wrangler python library to process input files uploaded to an s3 bucket using a Lambda function and store the processed files in an output s3 bucket. It has a glue crawler that programmatically update the processed file’s metadata to glue catalogue and create an Athena tables on top of the processed s3 files to enable users to run analytical queries on the dataset. 
`
The end-to-end orchestration is an event-driven approach. When an input file in .csv or .json format is uploaded to the ‘input s3 bucket’, it trigger a Lambda function that reads the file into a data frame. The script uses awsdatawrangler python library to perform transformation to manipulate the data, convert the data to parquet format, which triger glue crawler to update the Glue catalog with the metadata. Lambda writes the output paequet file to an ‘Output s3 bucket’ and the catalog table is created in Athena for SQL analysis. `

### Deploy the solution
1. cdk synth
2. cdk deploy
