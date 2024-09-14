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
             self.env.account, 
             self.env.region,
        ).get_stack_name(name)
    
    def get_resource_name(self, name: str,  resource_type: str = 'Resource') -> str:
        return self.scope.node.root.get_naming_strategy_cls()(
             self.scope.node.try_get_context('PRODUCT_PREFIX'),
             self.scope.node.try_get_context('STAGE'),
             self.env.account,
             self.env.region,
        ).get_resource_name(name, resource_type)
    
    def get_ssm_param_path_with_name(self, name: str) -> str:
        return self.scope.node.root.get_naming_strategy_cls()(
             self.scope.node.try_get_context('PRODUCT_PREFIX'),
             self.scope.node.try_get_context('STAGE'),
             self.env.account,
             self.env.region,
        ).get_ssm_param_path_with_name(name)
    
    def get_resource_logical_id(self, name: str, resource_type: str) -> str:
        return self.scope.node.root.get_naming_strategy_cls()(
             self.scope.node.try_get_context('PRODUCT_PREFIX'),
             self.scope.node.try_get_context('STAGE'),
             self.env.account,
             self.env.region,
        ).get_resource_logical_id(name, resource_type)