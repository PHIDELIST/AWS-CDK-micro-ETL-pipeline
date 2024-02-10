import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_micro_etl_pipeline.aws_cdk_micro_etl_pipeline_stack import AwsCdkMicroEtlPipelineStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_cdk_micro_etl_pipeline/aws_cdk_micro_etl_pipeline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsCdkMicroEtlPipelineStack(app, "aws-cdk-micro-etl-pipeline")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
