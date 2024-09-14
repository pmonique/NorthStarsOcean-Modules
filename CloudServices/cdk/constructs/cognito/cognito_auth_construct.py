
from aws_cdk import Stack, aws_ssm as ssm, aws_cognito as cognito
from constructs import Construct
from dataclasses import dataclass

from CloudServices.cdk.OceanConstruct import OceanConstruct
from CloudServices.cdk.OceanOptions import OceanOptions


class CognitoAuthConstruct(OceanConstruct):

    def __init__(self, scope: Construct, 
                 id: str, 
                 options: OceanOptions,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

  
        # Tworzenie User Pool
        user_pool = cognito.UserPool(self, self.ng.get_resource_logical_id(f"MainUserPool", "CognitoUserPool"),
            user_pool_name=options.UserPoolName.Ref,
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=options.SignInAliasesEmail.Ref),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=False),
                given_name=cognito.StandardAttribute(required=True, mutable=True)
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY
        )

        # Dodanie Hosted UI dla klienta webowego
        user_pool_client_web = user_pool.add_client(
            self.ng.get_resource_logical_id(f"WebClient", "UserPoolClient"),
            user_pool_client_name=options.ClientNameWeb.Ref,
            auth_flows=cognito.AuthFlow(user_password=True, user_srp=True),
            generate_secret=False,
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(authorization_code_grant=True),
                scopes=[cognito.OAuthScope.OPENID],
                callback_urls=[options.WebCallbackUrl.Ref],
                logout_urls=[options.WebLogoutUrl.Ref]
            )
        )

        # Dodanie Hosted UI dla klienta mobilnego
        user_pool_client_mobile = user_pool.add_client(
            self.ng.get_resource_logical_id(f"MobileClient", "UserPoolClient"), 
            user_pool_client_name=options.ClientNameMobile.Ref,
            auth_flows=cognito.AuthFlow(user_password=True, user_srp=True),
            generate_secret=False,
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(authorization_code_grant=True),
                scopes=[cognito.OAuthScope.OPENID],
                callback_urls=[options.MobileCallbackUrl.Ref],
                logout_urls=[options.MobileLogoutUrl.Ref]
            )
        )

        # Opcjonalnie: Dodaj domenę Hosted UI
        user_pool_domain = user_pool.add_domain(
            self.ng.get_resource_logical_id(f"CognitoDomain", "UserPoolDomain"),                                      
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix=options.DomainPrefix.Ref
            )
        )
