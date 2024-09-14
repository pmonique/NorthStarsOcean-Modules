import boto3
import dotenv
import os
from aws_cdk import Environment
from pprint import pprint


# TODO: path is wrong
dotenv.load_dotenv('.env')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'eu-west-2')


class OceanStartup:



    
    def __init__(self, startup_name, accounts):
        self.startup_name = startup_name
        self.tags = accounts[0]['Tags']  # Zakładamy, że tagi są takie same na wszystkich kontach
        self.environments = {
            'DEV': None,
            'QAE': None,
            'PROD': None,
            'Marketing': None
        }

        # Przypisanie kont AWS do odpowiednich środowisk na podstawie tagów
        for account in accounts:
            print(f"!!!! !!! Account: {account['Aws_account_id']} - Region: {account['Region']}")
            env_tag = account['Tags'].get('Environment')
            if env_tag and env_tag in self.environments:
                self.environments[env_tag] = Environment(
                    account=account['Aws_account_id'],
                    region=account['Region']  # Konto musi mieć tag Region -> może być lista regionów, a nie pojedynczy region TODO: obsłużyć to
                )

        self._initialize_environments(accounts)

    def _initialize_environments(self, accounts):
        """
        Inicjalizuje obiekty Environment dla kont przypisanych do odpowiednich środowisk.
        """
        for account in accounts:
            env_tag = account['Tags'].get('Environment')
            if env_tag and env_tag in self.environments:
                # TODO: poprawić tu, aby dopisywał listę środowisk, a nie nadpisywał ostatnie środowisko
                self.environments[env_tag] = Environment(
                    account=account['Aws_account_id'],
                    region=account['Region']
                )

        # Mapowanie do atrybutów obiektu
        for env_name in self.environments:
            setattr(self, env_name, self.environments[env_name])


    def get_environments(self, env_name) -> Environment:
        """
        Zwraca obiekt Environment dla danego środowiska (np. 'DEV', 'PROD').
        """
        return self.environments.get(env_name)  # TODO: obsłużyć brak środowiska, zwraca raczej Listę środowisk, bo środowisko, to numer konta + region, opakowane klasą cdk Environment() 
    

    def get_all_environments(self):
        """
        Zwraca listę wszystkich dostępnych środowisk dla startupu.
        """
        results = {k: v for k, v in self.environments.items() if v is not None}
        pprint(results)
        return results