from aws_cdk import aws_ssm as ssm
from constructs import Construct
from CloudServices.cdk.OceanOptions import OceanOptions
from CloudServices.cdk.OceanOptions import SSMParameterReference
from CloudServices.cdk.OceanConstruct import OceanConstruct

import logging

class SSMParametersConstruct(OceanConstruct):
    def __init__(self, scope: Construct, id: str, options: OceanOptions, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # TODO: resolve logger issue
        
        # self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(scope.get_logger_level())
        # Tworzenie parametrów SSM na podstawie opcji
        self.create_ssm_parameters(options)

    def create_ssm_parameters(self, options: OceanOptions) -> None:
        """
        Tworzy parametry SSM na podstawie pól z OceanOptions.
        
        :param options: Instancja OceanOptions zawierająca wartości i referencje do parametrów SSM.
        """
        for name, reference in options.__dict__.items():
            if isinstance(reference, SSMParameterReference):
                # Tworzenie parametru SSM na podstawie jego typu (String lub StringList)
                if isinstance(reference.value, list):
                    ssm.StringListParameter(
                        self,
                        self.ng.get_resource_logical_id(name, 'SSMParameter'),
                        parameter_name=self.ng.get_ssm_param_path_with_name(name),
                        string_list_value=reference.value,
                        description=f"SSM Parameter for {name}",
                        tier=ssm.ParameterTier.STANDARD
                    )
                elif isinstance(reference.value, str):
                    string_value = reference.value
                    print(f"Creating SSM parameter: {reference.value}")
                    if not isinstance(reference.value, str):
                        string_value = str(reference.value)
                    print(f"Creating SSM parameter: string_value: {string_value}")
                    ssm.StringParameter(
                        self,
                        self.ng.get_resource_logical_id(name, 'SSMParameter'),
                        parameter_name=self.ng.get_ssm_param_path_with_name(name),
                        string_value=string_value,
                        description=f"SSM Parameter for {name}",
                        tier=ssm.ParameterTier.STANDARD
                    )
                else: 
                    print(f"*** SSM Parameter {name} has unsupported type: {type(reference.value)}")
