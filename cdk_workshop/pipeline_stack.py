from constructs import Construct
from aws_cdk import (
    Stack,
    pipelines as pipelines,
)
from cdk_workshop.pipeline_stage import WorkshopPipelineStage


class WorkshopPipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Pipeline code goes here
        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                # input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                input=pipelines.CodePipelineSource.connection(
                    repo_string="IsraPR/cdk-workshop",
                    connection_arn="arn:aws:codeconnections:us-west-2:683172810798:connection/746a54aa-065d-4282-87d0-ba57b8c03ac2",  # noqa: E501
                    branch="main",
                ),
                commands=[
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild # noqa: E501
                    "pip install -r requirements.txt",  # Instructs Codebuild to install required packages# noqa: E501
                    "cdk synth",
                ],
            ),
        )
        deploy = WorkshopPipelineStage(self, "Deploy")
        deploy_stage = pipeline.add_stage(deploy)
        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestViewerEndpoint",
                env_from_cfn_outputs={"ENDPOINT_URL": deploy.hc_viewer_url},
                commands=["curl -Ssf $ENDPOINT_URL"],
            )
        )
        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestAPIGatewayEndpoint",
                env_from_cfn_outputs={"ENDPOINT_URL": deploy.hc_endpoint},
                commands=[
                    "curl -Ssf $ENDPOINT_URL",
                    "curl -Ssf $ENDPOINT_URL/hello",
                    "curl -Ssf $ENDPOINT_URL/test",
                ],
            )
        )
