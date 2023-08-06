from datetime import datetime, timezone

from paretos.authentication.access_token import AccessToken
from paretos.authentication.keycloak_service import KeycloakService


class KeycloakAuthenticator:
    def __init__(self, keycloak_service: KeycloakService, username: str, password: str):
        self.__keycloak_service = keycloak_service
        self.__username = username
        self.__password = password

    def __get_access_token(self):
        token = self.__keycloak_service.get_authentication_token(
            username=self.__username, password=self.__password
        )
        return token.get("access_token")

    def authenticate(self) -> AccessToken:
        access_token = self.__get_access_token()
        access_token_decoded = self.__keycloak_service.decode_token(access_token)

        expiration_date = datetime.fromtimestamp(
            access_token_decoded.get("exp"), tz=timezone.utc
        )

        return AccessToken(access_token, expiration_date)

    def get_customer_id(self) -> str:
        access_token = self.__get_access_token()
        access_token_decoded = self.__keycloak_service.decode_token(access_token)

        return access_token_decoded.get("customer_id")
