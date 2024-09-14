from aws_cdk import aws_ssm as ssm
from constructs import Construct
from CloudServices.cdk.OceanApp import OceanApp
from CloudServices.cdk.AWSResourceNameGenerator import AWSResourceNameGenerator


class OceanConstruct(Construct):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.ng = AWSResourceNameGenerator(scope)


    def create_ssm_parameter(self, param_name: str, string_value: str) -> ssm.StringParameter:
        """Helper function. 
                Creates an SSM parameter with the provided name and string value.

        Args:
            resource_prefix (str): Prefix of the resource. 
            param_name (str): Name of the parameter.
            string_value (str): Value of the parameter.

        Returns:
            ssm.StringParameter: The created SSM parameter.
        """
        return ssm.StringParameter(self, self.ng.get_resource_logical_id(param_name, "SSMParameter"),
            parameter_name=self.ng.get_ssm_param_path_with_name(param_name),
            string_value=string_value
        )


    def get_app(self) -> OceanApp:
        """
                Returns the OceanApp object associated with the stack.
        """
        parent_scope = self.node.scope  # from docs
        return parent_scope.get_app()
    
    def get_region(self) -> OceanApp:
        """
        Returns the REGION from OceanApp object associated with the scope.
        """
        parent_scope = self.node.scope  # from docs
        return parent_scope.get_app().get_region()
    
    def get_stage(self) -> OceanApp:
        """
        Returns the REGION from OceanApp object associated with the scope.
        """
        parent_scope = self.node.scope  # from docs
        return parent_scope.get_app().get_stage()
    
    def get_product_name(self) -> OceanApp:
        """
        Returns the REGION from OceanApp object associated with the scope.
        """
        parent_scope = self.node.scope  # from docs
        return parent_scope.get_app().get_product_name()