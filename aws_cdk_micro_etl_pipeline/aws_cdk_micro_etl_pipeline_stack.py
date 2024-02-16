from aws_cdk import (
    # Duration,
    Duration,
    Stack,
    # aws_sqs as sqs,
    CfnOutput,
    aws_iam as iam,
    aws_s3 as s3,
    RemovalPolicy,
    aws_glue as glue,
    aws_lambda as _lambda, 
    aws_s3_notifications as s3_notifications,
    aws_athena as athena,
    aws_sns as sns
)
from constructs import Construct


class AwsCdkMicroEtlPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "AwsCdkMicroEtlPipelineQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        input_s3_bucket="micro-etl-input"
        output_s3_bucket="micro-etl-output"
          # S3 Bucket to host glue scripts
        bucket_input = s3.Bucket(self, "RawDataS3bucket", bucket_name=input_s3_bucket,  versioned=False,
                           removal_policy=RemovalPolicy.DESTROY,
                           auto_delete_objects=True, block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
        bucket_output = s3.Bucket(self, "ProcessedDataS3bucket", bucket_name=output_s3_bucket, versioned=False,
                                  removal_policy=RemovalPolicy.DESTROY,
                                  auto_delete_objects=True, block_public_access=s3.BlockPublicAccess.BLOCK_ALL
                                  )
        # Lambda function for micro ETL
        micro_etl_lambda_role = iam.Role(
            self, 'MicroETLHandlerRole',
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal('lambda.amazonaws.com'),
                iam.ServicePrincipal('glue.amazonaws.com')
            )
        )
        # Allow Lambda function to write logs to CloudWatch
        micro_etl_lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                resources=["arn:aws:logs:*:*:*"]
            )
        )
                # Add permissions to the Lambda role
        micro_etl_lambda_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "s3:GetObject",
                "s3:PutObject",
                "athena:startQueryExecution",
                "athena:stopQueryExecution",
                "athena:getQueryExecution",
                "athena:getDataCatalog",
                "athena:getQueryResults",
                "glue:CreateDatabase", 
                "glue:GetDatabase",    
                "glue:UpdateDatabase", 
                "glue:DeleteDatabase", 
                "glue:CreateTable",    
                "glue:GetTable",       
                "glue:UpdateTable",    
                "glue:DeleteTable",    
                "glue:GetTables",      
                "glue:GetPartitions",  
                "glue:BatchDeletePartition", 
                "glue:CreatePartition",      
                "glue:DeletePartition",
                "glue:StartCrawler" 
            ],
            resources=["*"]
        ))

        # Policy to allow Lambda to read from input S3 bucket
        bucket_input.grant_read(micro_etl_lambda_role)

        # Policy to allow Lambda to write to output S3 bucket
        bucket_output.grant_write(micro_etl_lambda_role)


        # Lambda function for micro ETL using Docker image
        micro_etl_lambda = _lambda.DockerImageFunction(
            self, 'MicroETLHandler',
            function_name="MicroETLHandler",
            code=_lambda.DockerImageCode.from_image_asset('functions'),
            role=micro_etl_lambda_role,
            timeout= Duration.minutes(1) 
        )


        # S3 event notification to trigger the Lambda function
        bucket_input.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(micro_etl_lambda)
        )



        # Glue database
        micro_etl_glue_database = glue.CfnDatabase(
            self, "Microetldb",
            catalog_id="576997243977",
            database_input={"name": "microetldb"}
        )


        # Get the S3 bucket object from its name
        output_s3_bucket = s3.Bucket.from_bucket_name(self, "OutputS3Bucket", bucket_name="micro-etl-output")
        # Glue crawler
        micro_etl_crawler = glue.CfnCrawler(self, "MicroETLCrawler",
                                      role=micro_etl_lambda_role.role_arn,
                                      database_name= micro_etl_glue_database.catalog_id,
                                       targets={"s3Targets": [{"path": f"s3://{output_s3_bucket.bucket_name}/"}]}
                                      )

        # Athena workgroup
        micro_etl_athena_workgroup = athena.CfnWorkGroup(self, "MiroETLWorkGroup",
                                              name="MiroETLWorkGroup",
                                              work_group_configuration={
                                                  "publish_cloud_watch_metrics_enabled": True,
                                                  "enforce_work_group_configuration": True,
                                                  "bytes_scanned_cutoff_per_query": 100000000,
                                                  "requester_pays_enabled": False,
                                              },
                                               description="Athena workgroup for the Micro ETL pipeline")
        
        
        CfnOutput(scope=self, id='LambdaFunctionName', value=micro_etl_lambda.function_name)
        CfnOutput(scope=self, id='S3OutputBucketName', value=bucket_output.bucket_name)
        CfnOutput(scope=self, id='S3InputBucketName', value=bucket_input.bucket_name)
        CfnOutput(scope=self, id='GlueDatabaseName', value=micro_etl_glue_database.catalog_id)


