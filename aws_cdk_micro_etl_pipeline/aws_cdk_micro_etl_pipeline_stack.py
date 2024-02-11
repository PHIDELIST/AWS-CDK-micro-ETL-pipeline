from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam as iam,
    aws_s3 as s3,
    RemovalPolicy,
    aws_s3_deployment as s3deploy,
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

