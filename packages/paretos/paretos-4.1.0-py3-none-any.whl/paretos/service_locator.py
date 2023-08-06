from keycloak import KeycloakOpenID

from paretos import Config
from paretos.athena.athena_api_client import AthenaApiClient
from paretos.athena.athena_api_http_session import AthenaApiHttpSession
from paretos.authentication.access_token_provider import AccessTokenProvider
from paretos.authentication.keycloak_authenticator import KeycloakAuthenticator
from paretos.authentication.keycloak_service import KeycloakService
from paretos.command.export_handler import ExportHandler
from paretos.command.obtain_handler import ObtainHandler
from paretos.command.optimize_handler import OptimizeHandler
from paretos.command.predict_handler import PredictHandler
from paretos.command.use_case_handler import UseCaseHandler
from paretos.socrates.project_api_client import ProjectApiClient
from paretos.socrates.socrates_api_http_session import SocratesApiHttpSession
from paretos.use_case.use_case_api_client import UseCaseApiClient
from paretos.use_case.use_case_api_http_session import UseCaseApiHttpSession


class ServiceLocator:
    def __init__(self, config: Config):
        logger = config.get_logger()

        access_token_provider = AccessTokenProvider(
            KeycloakAuthenticator(
                KeycloakService(
                    KeycloakOpenID(
                        server_url=config.get_keycloak_server_url(),
                        realm_name=config.get_keycloak_realm_name(),
                        client_id=config.get_keycloak_socrates_api_client_id(),
                    )
                ),
                username=config.get_username(),
                password=config.get_password(),
            )
        )

        socrates_api_session = SocratesApiHttpSession(
            api_url=config.get_socrates_api_url(),
            access_token_provider=access_token_provider,
            logger=logger,
        )

        project_api_client = ProjectApiClient(socrates_api_session)

        self.__obtain_handler = ObtainHandler(
            logger=logger, api_client=project_api_client
        )

        self.__export_handler = ExportHandler(
            logger=logger, api_client=project_api_client
        )

        athena_api_session = AthenaApiHttpSession(
            api_url=config.get_athena_api_url(),
            api_name="Athena",
            access_token_provider=access_token_provider,
            logger=logger,
        )

        athena_api_client = AthenaApiClient(athena_api_session)

        self.__predict_handler = PredictHandler(
            logger=logger, api_client=athena_api_client
        )

        use_case_api_session = UseCaseApiHttpSession(
            api_url=config.get_use_case_api_url(),
            access_token_provider=access_token_provider,
            logger=logger,
        )

        use_case_api_client = UseCaseApiClient(use_case_api_session)

        self.__optimize_handler = OptimizeHandler(
            logger=logger,
            api_client=project_api_client,
            use_case_api_client=use_case_api_client,
        )

        self.__use_case_handler = UseCaseHandler(
            logger=logger, api_client=use_case_api_client
        )

    @property
    def optimize_handler(self) -> OptimizeHandler:
        return self.__optimize_handler

    @property
    def export_handler(self) -> ExportHandler:
        return self.__export_handler

    @property
    def obtain_handler(self) -> ObtainHandler:
        return self.__obtain_handler

    @property
    def predict_handler(self) -> PredictHandler:
        return self.__predict_handler

    @property
    def use_case_handler(self) -> UseCaseHandler:
        return self.__use_case_handler
