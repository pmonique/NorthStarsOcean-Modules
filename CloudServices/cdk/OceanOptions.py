from aws_cdk import aws_ssm as ssm
from constructs import Construct
from typing import Any, Dict
from CloudServices.cdk.OceanConstruct import AWSResourceNameGenerator
import yaml

from pathlib import Path
from typing import Dict, Any


class SSMParameterReference:
    def __init__(self, value: Any, ref: str) -> None:
        self._value = value
        self.Ref = ref

    @property
    def value(self):
        return self._value

    def __getattr__(self, name: str) -> Any:
        # If trying to access anything other than .Ref, return the value
        if name == 'value':
            return self._value
        raise AttributeError(f"'SSMParameterReference' object has no attribute '{name}'")

    def __str__(self):
        return str(self._value)

class OceanOptions:
    def __init__(self, scope: Construct, class_name: str) -> None:
        self.scope = scope
        self.class_name = class_name
        
        # load from file yaml all values for class_name
        self.instance_values = self.__load_from_file()

        self.ng = AWSResourceNameGenerator(scope)

        # Dynamically add attributes based on instance_values
        for name, value in self.instance_values.items():
            ref_value = self.create_ssm_ref(name, value)
            self.__dict__[name] = SSMParameterReference(value, ref_value)

    def create_ssm_ref(self, name: str, value: Any) -> str:
        """Creates an SSM parameter reference."""

        ssm_param_name = self.ng.get_ssm_param_path_with_name(name)

        if isinstance(value, list):
            return ssm.StringListParameter.value_for_string_list_parameter(self.scope, ssm_param_name)
        elif isinstance(value, str):
            return ssm.StringParameter.value_for_string_parameter(self.scope, ssm_param_name)
        elif isinstance(value, dict):  # TODO: check if this is correct for all values
            return ssm.StringParameter.value_for_string_parameter(self.scope, ssm_param_name)
        else:
            return value  # Bool values shouldnt be processed as SSM Params, but hardcoded in cdk.out template TODO: check if this is correct for all values

    def __getattr__(self, name: str) -> Any:
        """Allows access to dynamically created attributes."""
        if name in self.__dict__:
            return self.__dict__[name].value  # Return the value directly
        raise AttributeError(f"'{self.class_name}' object has no attribute '{name}'")

    def __load_from_file(self) -> Dict[str, Any]:
        """Loads instance values from a YAML file."""   
        
        print("Loading instance values from YAML file...")
         
        # Dynamiczne wykrywanie ścieżki do katalogu głównego projektu
        project_root = Path(__file__).resolve().parent.parent.parent.parent  # dostosuj do struktury projektu
        # Składanie ścieżki względnej względem katalogu głównego projektu
        file_path = project_root / f"Products/{self.scope.get_product_name()}/API/data/{self.scope.get_stage()}/{self.class_name}.{self.scope.get_stage()}.{self.scope.get_region()}.yaml"
        
        # Wczytywanie danych z pliku YAML
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)


        print(f"Loaded data from {file_path}:")
        return data
