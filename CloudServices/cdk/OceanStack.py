from aws_cdk import Stack, Environment
from constructs import Construct
from CloudServices.cdk.OceanApp import OceanApp
 



class OceanStack(Stack):
    def __init__(self, scope: Construct, id: str, env: Environment=None, **kwargs) -> None:
        super().__init__(scope, id, env=env, *kwargs)

    def get_app(self) -> OceanApp:
        """
        Returns the OceanApp object associated with the stack.
        """
        return self.node.root
    
