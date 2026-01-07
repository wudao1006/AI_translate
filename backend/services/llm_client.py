"""
LLM client with provider-agnostic interface and multiple provider support.
Uses official SDKs: OpenAI SDK for OpenAI-compatible APIs, Anthropic SDK for Claude.
"""
from abc import ABC, abstractmethod
from typing import Optional
from openai import OpenAI
from anthropic import Anthropic

from config import settings
from utils.logging import get_logger

logger = get_logger(__name__)


class LLMResponse:
    """Standardized LLM response."""

    def __init__(self, content: str, raw_response: Optional[dict] = None):
        self.content = content
        self.raw_response = raw_response


class BaseLLMProvider(ABC):
    """Base class for LLM providers."""

    def __init__(self, api_key: str, model: str, timeout: int, base_url: str = ""):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.base_url = base_url

    @abstractmethod
    async def chat(self, messages: list[dict]) -> LLMResponse:
        """Send chat request to LLM provider."""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI-compatible provider using official OpenAI SDK.

    Supports:
    - OpenAI (default)
    - Moonshot (Kimi)
    - DeepSeek
    - Any OpenAI-compatible API
    """

    def __init__(self, api_key: str, model: str, timeout: int, base_url: str = ""):
        super().__init__(api_key, model, timeout, base_url)

        # Initialize OpenAI client
        client_kwargs = {
            "api_key": api_key,
            "timeout": float(timeout),
        }

        # Use custom base URL if provided
        if base_url:
            client_kwargs["base_url"] = base_url

        self.client = OpenAI(**client_kwargs)

    async def chat(self, messages: list[dict]) -> LLMResponse:
        """Call OpenAI-compatible chat completion API using SDK."""
        try:
            # Call OpenAI API using SDK
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content

            # Convert response to dict for raw_response
            raw_response = {
                "id": response.id,
                "model": response.model,
                "choices": [
                    {
                        "message": {
                            "role": response.choices[0].message.role,
                            "content": content,
                        },
                        "finish_reason": response.choices[0].finish_reason,
                    }
                ],
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0,
                },
            }

            return LLMResponse(content=content, raw_response=raw_response)

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise


class ClaudeProvider(BaseLLMProvider):
    """Anthropic Claude provider using official Anthropic SDK."""

    def __init__(self, api_key: str, model: str, timeout: int, base_url: str = ""):
        super().__init__(api_key, model, timeout, base_url)

        # Initialize Anthropic client
        client_kwargs = {
            "api_key": api_key,
            "timeout": float(timeout),
        }

        # Use custom base URL if provided
        if base_url:
            client_kwargs["base_url"] = base_url

        self.client = Anthropic(**client_kwargs)

    async def chat(self, messages: list[dict]) -> LLMResponse:
        """Call Claude messages API using SDK."""
        try:
            # Convert messages format (Claude expects system separately)
            system_message = None
            user_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    user_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            # Call Claude API using SDK
            kwargs = {
                "model": self.model,
                "max_tokens": 1024,
                "messages": user_messages,
                "temperature": 0.3,
            }

            if system_message:
                kwargs["system"] = system_message

            response = self.client.messages.create(**kwargs)

            content = response.content[0].text

            # Convert response to dict for raw_response
            raw_response = {
                "id": response.id,
                "model": response.model,
                "content": [{"type": "text", "text": content}],
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                },
            }

            return LLMResponse(content=content, raw_response=raw_response)

        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            raise


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek provider (OpenAI-compatible)."""

    def __init__(self, api_key: str, model: str, timeout: int, base_url: str = ""):
        # Set default DeepSeek base URL if not provided
        if not base_url:
            base_url = "https://api.deepseek.com/v1"
        super().__init__(api_key, model, timeout, base_url)


class QwenProvider(OpenAIProvider):
    """Qwen (Tongyi Qianwen) provider (OpenAI-compatible)."""

    def __init__(self, api_key: str, model: str, timeout: int, base_url: str = ""):
        # Set default Qwen base URL if not provided
        if not base_url:
            base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        super().__init__(api_key, model, timeout, base_url)


class LLMClient:
    """Main LLM client with provider selection."""

    def __init__(self):
        self.provider = self._create_provider()

    def _create_provider(self) -> BaseLLMProvider:
        """Create provider instance based on configuration."""
        provider_map = {
            "openai": OpenAIProvider,
            "claude": ClaudeProvider,
            "deepseek": DeepSeekProvider,
            "qwen": QwenProvider,
        }

        provider_class = provider_map.get(settings.llm_provider)
        if not provider_class:
            raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")

        logger.info(f"Initializing LLM provider: {settings.llm_provider}")
        logger.info(f"Model: {settings.llm_model}")
        if settings.llm_base_url:
            logger.info(f"Base URL: {settings.llm_base_url}")

        return provider_class(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
            timeout=settings.llm_timeout,
            base_url=settings.llm_base_url,
        )

    async def chat(self, messages: list[dict]) -> LLMResponse:
        """Send chat request through configured provider."""
        try:
            return await self.provider.chat(messages)
        except Exception as e:
            logger.error(f"LLM client error: {str(e)}")
            raise


# Global LLM client instance
llm_client = LLMClient()
