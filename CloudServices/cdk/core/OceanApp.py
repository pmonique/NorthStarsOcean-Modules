#!/usr/bin/env python3
import os

from aws_cdk import App
from dotenv import load_dotenv, dotenv_values
# from CloudServices.cdk.AWSResourceNameGenerator import AWSResourceNameGenerator
from CloudServices.cdk.core.OceanContext import OceanContext
from CloudServices.cdk.core.OceanNamingStrategy import OceanNamingStrategy
from CloudServices.cdk.core import OceanContext
import logging
import os
from dotenv import load_dotenv
from pathlib import Path
from aws_cdk import App, Stack, Environment
from typing import Optional, Type
from constructs import Construct


class OceanApp(App):

    
    REQUIRED_CONTEXT_KEYS = ['STAGE', 'PRODUCT_PREFIX'] # check file .env.* for ontext keys and values

    def __init__(self, ocean_context: OceanContext, naming_strategy_cls: Type[OceanNamingStrategy], required_context_keys=[], **kwargs) -> None:
        super().__init__(**kwargs)

        self.REQUIRED_CONTEXT_KEYS += required_context_keys
        self._context_keys = []

        if not issubclass(naming_strategy_cls, OceanNamingStrategy):
            raise ValueError("OceanApp->naming_strategy must be a subclass of OceanNamingStrategy")

        # Przekazujemy jedynie strategię, a sama instancja jest per Stack ponieważ wymaga zmiennej env:Environment // account id, region etc.
        # Ustawienie kontekst 
        self._set_node_context(ocean_context)

        self.naming_strategy_cls = naming_strategy_cls 
        

    def validate(self) -> None:
        """Wywołaj tę metodę po zakończeniu inicjalizacji aplikacji, aby przeprowadzić walidację kontekstu."""
        self._validate_context()
   
    def _set_node_context(self, ocean_context: OceanContext) -> None:
        """Ustawia wartości kontekstowe w aplikacji CDK na podstawie konfiguracji."""
        print(f"Setting AWS App context: {ocean_context.config.items()}")
        for key, value in ocean_context.config.items():
            print(f"Trying to set AWS App context: {key}={value}")
            self._context_keys.append(key)

            if value is not None:
                self.node.set_context(key, value)
                print(f"Setting AWS App context: {key}={value} for {type(self)}")
                print(f"Checking AWS App context: FOR {key} EXPECTED {value} THEN {self.node.try_get_context(key)}")
        
        

    def get_naming_strategy_cls(self) -> OceanNamingStrategy:
        """Zwraca strategię nadawania nazw."""
        return self.naming_strategy_cls
    
    def _validate_context(self) -> None:
        """Waliduje kontekst w aplikacji CDK."""
        # Implementacja walidacji kontekstu
        for required_key in self.REQUIRED_CONTEXT_KEYS:
             
            print(f" >>> ================= > > > > > Checking required context key: {required_key} => {self.node.try_get_context(required_key)} <<<<< ")
            if self.node.try_get_context(required_key) is None:
                raise ValueError(f"Required context key '{required_key}' not found.")
 