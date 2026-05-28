import pytest

from payment_api.core.config import Settings


@pytest.fixture
def mock_settings() -> Settings:
    return Settings(
        database_url="postgresql+asyncpg://test:test@localhost:5432/test",
        rabbitmq_url="amqp://test:test@localhost:5672/",
        api_key="TEST_API_KEY",
    )
