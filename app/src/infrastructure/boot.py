from dotenv import load_dotenv
from pydm import ServiceContainer, EnvParametersBag
from app.src.domain.review.service.n8n_client import N8nClientInterface
from app.src.infrastructure.n8n.sdk import N8nSDK, N8nClient

def boot() -> None:
    service_container: ServiceContainer = ServiceContainer.get_instance()

    load_dotenv()
    service_container.set_parameters(EnvParametersBag())

    service_container.bind_parameters(N8nSDK, {'base_url': 'N8N_BASE_URL'})
    service_container.bind_parameters(N8nClient, {'code_reviewer_webhook_path': 'N8N_CODE_REVIEWER_WEBHOOK_PATH'})
    service_container.bind(N8nClientInterface, N8nClient)