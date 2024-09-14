import os
import json
from pathlib import Path
from typing import Optional, Dict
from aws_cdk import App
from dotenv import dotenv_values


class OceanContext:
    def __init__(self, config_path: Optional[str] = None, env_file_path: Optional[str] = None) -> None:
        self.config = {}
        self.env_file_path = env_file_path

        if config_path:
            self.load_config_from_json(config_path)
        if env_file_path:
            self.load_env_variables(env_file_path)
        self.load_environment_variables()

    def load_config_from_json(self, path: str) -> None:
        """Ładuje konfigurację z pliku JSON."""
        with open(path, 'r') as file:
            self.config.update(json.load(file))

    def load_env_variables(self, path: str) -> None:
        """Ładuje zmienne środowiskowe z pliku .env."""
        self.config = dotenv_values(path)
        print(f"Loading environment variables from {path}")
    
    def load_environment_variables(self) -> None:
        """Ładuje systemowe zmienne środowiskowe do słownika config. 
        Uzyteczne do CI/CD"""
        self.config.update({})
        # TODO: adaptation for CI/CD env.

    def get(self, key: str) -> Optional[str]:
        """Zwraca wartość dla danego klucza z konfiguracji."""
        return self.config.get(key)

    def get_required(self, key: str) -> str:
        """Zwraca wartość dla danego klucza lub zgłasza błąd, jeśli klucz nie istnieje."""
        value = self.get(key)
        if value is None:
            raise ValueError(f"Required configuration key '{key}' not found.")
        return value

    def set_context(self, app: App) -> None:
        """Ustawia konfigurację w kontekście CDK."""
        for key, value in self.config.items():
            app.node.set_context(key, value)
 