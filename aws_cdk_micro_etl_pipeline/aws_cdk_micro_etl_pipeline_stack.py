from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    CfnOutput,
    aws_iam as iam,
    aws_s3 as s3,
    RemovalPolicy,
    aws_s3_deployment as s3deploy,
    aws_lambda as _lambda, 
    aws_s3_notifications as s3_notifications
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
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
        )
          # Allow Lambda function to write logs to CloudWatch
        micro_etl_lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                resources=["arn:aws:logs:*:*:*"]
            )
        )
        # Attach policy to allow Lambda to read from input S3 bucket
        bucket_input.grant_read(micro_etl_lambda_role)

        # Attach policy to allow Lambda to write to output S3 bucket
        bucket_output.grant_write(micro_etl_lambda_role)

    
        # micro_etl_lambda = _lambda.Function(
        #     self, 'MicroETLHandler',
        #     function_name="MicroETLHandler",
        #     runtime=_lambda.Runtime.PYTHON_3_10,
        #     code=_lambda.Code.from_asset('functions'),
        #     handler='csv_to_parquet_lambda.lambda_handler',
        #     role=micro_etl_lambda_role
        # )
         # Lambda function for micro ETL using Docker image
        micro_etl_lambda = _lambda.DockerImageFunction(
            self, 'MicroETLHandler',
            function_name="MicroETLHandler",
            code=_lambda.DockerImageCode.from_image_asset('functions'),
            role=micro_etl_lambda_role
        )


             # Configure S3 event notification to trigger the Lambda function
        bucket_input.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(micro_etl_lambda)
            #"Event to trigger csv to parquet lambda converter"
        )

           # CDK Outputs
        CfnOutput(scope=self, id='LambdaFunctionName', value=micro_etl_lambda.function_name)
        CfnOutput(scope=self, id='S3OutputBucketName', value=bucket_output.bucket_name)
        CfnOutput(scope=self, id='S3InputBucketName', value=bucket_input.bucket_name)


