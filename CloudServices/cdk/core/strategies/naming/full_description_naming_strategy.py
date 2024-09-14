from CloudServices.cdk.core.OceanNamingStrategy import OceanNamingStrategy


class FullDescriptionNamingStrategy(OceanNamingStrategy):
    """Generates names and paths for AWS resources based on individual string parameters."""
    

    def __init__(self, product_prefix: str, deployment_stage: str, aws_account_id: str, aws_region: str) -> None:
        """Inicjalizuje strategię pełnej ścieżki z indywidualnymi parametrami typu string."""
        print(f"Product prefix: {product_prefix}")
        print(f"Deployment stage: {deployment_stage}")
        print(f"AWS Account ID: {aws_account_id}")
        print(f"AWS Region: {aws_region}")
        

        self.cdk_resource_prefix = f"{product_prefix}{self.DELIMITER}{deployment_stage}{self.DELIMITER}{aws_account_id}{self.DELIMITER}{aws_region}"
        self.cdk_stack_name_prefix = self.cdk_resource_prefix
        self.cdk_params_path = f"/params/{self.cdk_resource_prefix.replace(self.DELIMITER, self.PATH_DELIMITER)}/"

    def get_stack_name(self, name: str) -> str:
        """Zwraca nazwę stosu (stack)."""
        return f"{self.cdk_stack_name_prefix}{self.DELIMITER}{name}{self.DELIMITER}Stack"

    def get_resource_name(self, name: str, resource_type: str) -> str:
        """Zwraca nazwę zasobu."""
        return f"{self.cdk_resource_prefix}{self.DELIMITER}{name}{self.DELIMITER}{resource_type}"

    def get_ssm_param_path_with_name(self, name: str) -> str:
        """Zwraca ścieżkę parametru SSM."""
        return f"{self.cdk_params_path}{name}"
    
    def get_resource_logical_id(self, name: str, resource_type: str) -> str:
        """Zwraca logiczny identyfikator zasobu."""
        return f"{name}{resource_type}LogicalId"
