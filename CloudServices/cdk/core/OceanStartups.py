import boto3
from CloudServices.cdk.core.OceanStartup import OceanStartup
from CloudServices.cdk.core.OceanContext import OceanContext
from typing import Dict, List


AWS_DEFAULT_REGION = 'eu-west-2'

class OceanStartups:
    def __init__(self, context: OceanContext):
        print("Initializing AWS access for OceanStartups...")
        self.client = boto3.client('organizations')
        self._check_aws_access()
        self.startups = self.fetch_startups_from_aws()

    def _check_aws_access(self):
        """Metoda sprawdzająca dostęp do AWS."""
        print("Checking AWS access for OceanStartups...")
        try:
            self.client.list_roots()
            print("Successfully connected to AWS for OceanStartups.")
        except Exception as e:
            print("Failed to connect to AWS for OceanStartups:", e)
            raise

    def fetch_startups_from_aws(self):
        """
        Pobiera listę startupów i ich środowisk na podstawie struktury folderów i tagów w AWS Organizations.
        """
        startups_dict = {}
        paginator = self.client.get_paginator('list_accounts')
        response_iterator = paginator.paginate()

        for response in response_iterator:
            for account in response['Accounts']:
                account_id = account['Id']
                account_name = account['Name']

                # Pobranie tagów dla konta
                tags_response = self.client.list_tags_for_resource(ResourceId=account_id)
                tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}

                startup_name = tags.get('Startup')
                environment = tags.get('Environment')

                if startup_name and environment:
                    if startup_name not in startups_dict:
                        startups_dict[startup_name] = []

                    startups_dict[startup_name].append({
                        'Aws_account_id': account_id,
                        'Name': account_name,
                        'Tags': tags,
                        'Region': tags.get('Region', AWS_DEFAULT_REGION)
                    })

        # Tworzymy obiekty OceanStartup
        return {name: OceanStartup(name, accounts) for name, accounts in startups_dict.items()}

    def get_startup(self, startup_name):
        """
        Zwraca obiekt OceanStartup na podstawie nazwy startupu.
        """
        return self.startups.get(startup_name)

    def get_all_startups(self) -> dict:
        """
        Zwraca słownik wszystkich startupów.
        """
        return self.startups
