from constructs import Construct


# class AWSResourceNameGenerator:
#     """Generates names for AWS resources based on the given prefix and configuration."""
#     DELIMITER = "-"
#     PATH_DELIMITER = "/"

#     def __init__(self, prefix: str, deployment_stage: str, aws_account_id: str, aws_region: str) -> None:
#         self.cdk_resource_prefix = f"{prefix}{self.DELIMITER}{deployment_stage}{self.DELIMITER}{aws_account_id}{self.DELIMITER}{aws_region}"
#         self.cdk_stack_name_prefix = self.cdk_resource_prefix
#         self.cdk_params_path = f"/params/{self.cdk_resource_prefix.replace(self.DELIMITER, '/')}/"

#     def get_stack_name(self, name: str) -> str:
#         """Generates a name for a stack."""
#         return f"{self.cdk_stack_name_prefix}{self.DELIMITER}{name}{self.DELIMITER}Stack"

#     def get_resource_name(self, name: str, resource_type: str) -> str:
#         """Generates a name for a resource."""
#         return f"{self.cdk_resource_prefix}{self.DELIMITER}{name}{self.DELIMITER}{resource_type}"

#     def get_ssm_param_path_with_name(self, name: str) -> str:
#         """Generates a name for an SSM parameter."""
#         return f"{self.cdk_params_path}{name}"
    
#     def get_resource_logical_id(self, name: str, resource_type: str) -> str:
#         """Generates a name for a resource."""
#         return f"{name}{resource_type}LogicalId"
    


class AWSResourceNameGenerator:
    """Generates names for AWS resources based on the app's configuration."""
    DELIMITER = "-"
    PATH_DELIMITER = "/"

    def __init__(self, scope: Construct) -> None:
        # Zakładamy, że scope jest OceanApp lub jego pochodną
        app = scope.get_app()

        # Calculated values    
        self.cdk_resource_prefix = f"{app.product_prefix}{self.DELIMITER}{app.deployment_stage}{self.DELIMITER}{app.aws_account_id}{self.DELIMITER}{app.aws_region}"
        self.cdk_stack_name_prefix = self.cdk_resource_prefix
        self.cdk_params_path = f"/params/{self.cdk_resource_prefix.replace(self.DELIMITER, '/')}/"

    def get_stack_name(self, name: str) -> str:
        """Generates a name for a stack."""
        return f"{self.cdk_stack_name_prefix}{self.DELIMITER}{name}{self.DELIMITER}Stack"

    def get_resource_name(self, name: str, resource_type:str) -> str:
        """Generates a name for a resource."""
        return f"{self.cdk_resource_prefix}{self.DELIMITER}{name}{self.DELIMITER}{resource_type}"

    def get_ssm_param_path_with_name(self, name: str) -> str:
        """Generates a name for an SSM parameter."""
        return f"{self.cdk_params_path}{name}"
    
    def get_resource_logical_id(self, name: str, resource_type:str) -> str:
        """Generates a name for a resource."""
        return f"{name}{resource_type}LogicalId"

 