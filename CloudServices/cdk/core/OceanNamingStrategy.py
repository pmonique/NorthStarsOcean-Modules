from abc import ABC, abstractmethod
from aws_cdk import Environment
from constructs import Construct


class OceanNamingStrategy(ABC):
    """Abstrakcyjna klasa bazowa dla strategii nazw zasobów AWS."""

    DELIMITER = "-"
    PATH_DELIMITER = "/"

    def __init__(self, node: Construct , env:Environment) -> None:
        
        self.node = node
        self.env = env

        self.product_prefix = node.try_get_context("AWS_PRODUCT_PREFIX")  
        self.account_id = env.account.account_id
        self.region = env.account.region
        self.stage = node.try_get_context("STAGE")  


    
    @abstractmethod
    def get_stack_name(self, name: str) -> str:
        """Zwraca nazwę stosu (stack)."""
        pass

    @abstractmethod
    def get_resource_name(self, name: str, resource_type: str) -> str:
        """Zwraca nazwę zasobu."""
        pass

    @abstractmethod
    def get_ssm_param_path_with_name(self, name: str) -> str:
        """Zwraca ścieżkę parametru SSM."""
        pass
    
    @abstractmethod
    def get_resource_logical_id(self, name: str, resource_type: str) -> str:
        """Zwraca logiczny identyfikator zasobu."""
        pass
