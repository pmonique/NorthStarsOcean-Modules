import boto3
import dotenv
import os
from aws_cdk import Environment


AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'eu-west-2')


class OceanEnvironments:

    def __init__(self):
        # Komunikat o inicjalizacji dostępu do AWS
        print("Initializing AWS access for OceanEnvironments...")

        # Inicjalizujemy klienta boto3 dla AWS Organizations
        self.client = boto3.client('organizations')

        # Sprawdzenie dostępu do konta AWS
        self._check_aws_access()

        # Pobieramy środowiska
        self.environments = self.fetch_environments_from_aws()

    def _check_aws_access(self):
        """Metoda sprawdzająca dostęp do AWS."""
        try:
            # Wykonujemy prostą operację, aby sprawdzić połączenie
            self.client.list_roots()
            print("Successfully connected to AWS for OceanEnvironments.")
        except Exception as e:
            print("Failed to connect to AWS for OceanEnvironments:", e)
            raise

    def fetch_environments_from_aws(self):
        """
        Pobiera listę kont w organizacji z AWS Organizations i zwraca listę słowników ze szczegółami.
        
        :return: Lista środowisk z kontami AWS.
        """
        response = self.client.list_accounts()
        
        environments_list = []
        paginator = self.client.get_paginator('list_accounts')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            
            for account in response['Accounts']:

                account_id = account['Id']
                account_name = account['Name']

                # Pobranie tagów dla konta
                tags_response = self.client.list_tags_for_resource(ResourceId=account_id)

                tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}

                # Zakładając, że "region" i "startup" są dostępne jako tagi w koncie
                region = tags.get('Region', AWS_DEFAULT_REGION ) # Domyślny region, jeśli nie ma tagu
                startup = tags.get('Startup', account_name)

                # Check if there are more tags to fetch
                while 'NextToken' in tags_response:
                    tags_response = self.client.list_tags_for_resource(ResourceId=account_id, NextToken=tags_response['NextToken'])
                    tags.update({tag['Key']: tag['Value'] for tag in tags_response['Tags']})

                
                environments_list.append({
                    'Aws_account_id': account_id,
                    'Name': account_name,
                    'Tags': tags,
                    'Region': region,
                    'Startup': startup
                })
        
        return environments_list

    def filter_by_name(self, account_name_partial):
        """
        Filtruje listę środowisk na podstawie podanego parametru.
        
        :param param_name: Nazwa parametru do filtrowania.
        :param param_value: Wartość parametru, na podstawie której filtrujemy listę.
        :return: Lista środowisk (słowników), które spełniają kryterium filtrowania.
        """
        return [
            env for env in self.environments
            if account_name_partial.upper() in env.get('Name').upper()
        ]
    
    def filter_by_param(self, param_name, param_value):
        """
        Filtruje listę środowisk na podstawie podanego parametru.
        
        :param param_name: Nazwa parametru do filtrowania.
        :param param_value: Wartość parametru, na podstawie której filtrujemy listę.
        :return: Lista środowisk (słowników), które spełniają kryterium filtrowania.
        """
        return [
            env for env in self.environments
            if env.get(param_name) == param_value
        ]

    def get_environment_objects(self, param_name, param_value=None):
        """
        Zwraca listę obiektów Environment dla środowisk, które spełniają kryterium filtrowania.
        
        :param param_name: Nazwa parametru do filtrowania.
        :param param_value: Wartość parametru, na podstawie której filtrujemy listę.
        :return: Lista obiektów Environment.
        """
        

        filtered_envs = self.environments

        if param_value is None and param_name is not None:
            filtered_envs = self.filter_by_name(param_name)
        
        elif param_name is not None:
            filtered_envs = self.filter_by_param(param_name, param_value)
        
        # TODO: Regions -> Region map Regions: [region1, region2, ...] 
        return [
            Environment(account=env['Aws_account_id'], region=env['Region'])
            for env in filtered_envs
        ]


# Example:
# envs = Environments()
# print( envs.get_environment_objects('MTAI') )



