import aws_cdk as cdk
from cdk_workshop.pipeline_stack import WorkshopPipelineStack

app = cdk.App()
WorkshopPipelineStack(
    app,
    "WorkshopPipelineStack",
    env=cdk.Environment(account="683172810798", region="us-west-2"),
)

app.synth()
