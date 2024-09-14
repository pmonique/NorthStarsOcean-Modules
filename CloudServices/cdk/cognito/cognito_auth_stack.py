from aws_cdk import Stack
from aws_cdk import aws_ssm as ssm
from dataclasses import dataclass
from constructs import Construct

from CloudServices.cdk.core.OceanStack import OceanStack
from CloudServices.cdk.core.OceanOptions import OceanOptions
from CloudServices.cdk.ssm.ssm_parameters_construct import SSMParametersConstruct
from CloudServices.cdk.cognito.cognito_auth_construct import CognitoAuthConstruct


class CognitoAuthStack(OceanStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        
        cognito_options = OceanOptions(self, "CognitoAuthOptions")
        print(f"Cognito options: {cognito_options.instance_values}")

        SSMParametersConstruct(self, "CognitoAuthParams", options=cognito_options)
        CognitoAuthConstruct(self, "CognitoAuth", options=cognito_options)


        