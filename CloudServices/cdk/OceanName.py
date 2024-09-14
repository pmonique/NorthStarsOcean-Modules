from aws_cdk import (
    Environment
)
from constructs import Construct



class OceanName:

    def __init__(self, scope: Construct, env: Environment) -> None:
        self.scope = scope
        self.env = env
        self.naming_strategy = scope.node.root.get_naming_strategy_cls()

    
    def get_stack_name(self, name: str) -> str:
        return self.scope.node.root.get_naming_strategy_cls()(
             self.scope.node.try_get_context('PRODUCT_PREFIX'), 
             self.scope.node.try_get_context('STAGE'), 
             self.scope.node.try_get_context('AWS_ACCOUNT_ID'), 
             self.scope.node.try_get_context('AWS_REGION') 
        ).get_stack_name(name)