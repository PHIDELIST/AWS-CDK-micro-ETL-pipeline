from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam as iam,
    aws_s3 as s3,
    RemovalPolicy,
    aws_s3_deployment as s3deploy,
    aws_lambda as _lambda, 
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
        
        # Attach policy to allow Lambda to read from input S3 bucket
        bucket_input.grant_read(micro_etl_lambda_role)

        # Attach policy to allow Lambda to write to output S3 bucket
        bucket_output.grant_write(micro_etl_lambda_role)
        
        micro_etl_lambda = _lambda.Function(
            self, 'MicroETLHandler',
            function_name="MicroETLHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('functions'),
            handler='csv_to_parquet_lambda.lambda_handler',
            role=micro_etl_lambda_role
        )

           # CDK Outputs
        CfnOutput(scope=self, id='LambdaFunctionName', value=micro_etl_lambda.function_name)
        CfnOutput(scope=self, id='S3OutputBucketName', value=bucket_output.bucket_name)
        CfnOutput(scope=self, id='S3InputBucketName', value=bucket_input.bucket_name)


