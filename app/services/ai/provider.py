from app.core.config import get_settings
from app.services.ai.base import AIProvider
from app.services.ai.mock_provider import MockAIProvider


def get_ai_provider() -> AIProvider:
    settings = get_settings()
    if settings.AI_PROVIDER == "mock":
        return MockAIProvider()
    raise ValueError(f"Unsupported AI provider: {settings.AI_PROVIDER}")
