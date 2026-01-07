"""
Translation service - core business logic.
Orchestrates prompt building, LLM calls, and response parsing.
"""
import json
from typing import Tuple

from services.llm_client import llm_client
from utils.logging import get_logger

logger = get_logger(__name__)


class TranslationError(Exception):
    """Custom exception for translation failures."""

    pass


class Translator:
    """Translation service with keyword extraction."""

    SYSTEM_PROMPT = """You are a professional translation assistant.
Your task is to translate Chinese text to English and extract key concepts.
Always respond with valid JSON only, no additional text.
JSON format: {"translation": "English text here", "keywords": ["word1", "word2", "word3"]}
Extract 3-5 most important keywords from the Chinese text."""

    def _build_messages(self, chinese_text: str) -> list[dict]:
        """Build messages for LLM request."""
        user_prompt = f"""Translate the following Chinese text to English and extract 3-5 keywords.
Return only valid JSON with keys "translation" and "keywords".

Chinese text:
{chinese_text}"""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

    def _parse_response(self, content: str) -> Tuple[str, list[str]]:
        """Parse LLM response to extract translation and keywords."""
        try:
            # Try to parse as JSON directly
            data = json.loads(content)
            translation = data.get("translation", "").strip()
            keywords = data.get("keywords", [])

            if not translation:
                raise ValueError("Missing translation in response")
            if not keywords or len(keywords) < 3:
                raise ValueError("Invalid keywords: must have 3-5 items")

            # Ensure 3-5 keywords
            keywords = keywords[:5]
            if len(keywords) < 3:
                raise ValueError(f"Too few keywords: {len(keywords)}")

            return translation, keywords

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.debug(f"Raw response: {content}")
            raise TranslationError(f"Invalid JSON response from LLM: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Invalid response structure: {e}")
            raise TranslationError(f"Invalid response structure: {str(e)}")

    async def translate(self, chinese_text: str) -> Tuple[str, list[str]]:
        """
        Translate Chinese text to English and extract keywords.

        Args:
            chinese_text: Input text in Chinese

        Returns:
            Tuple of (translation, keywords)

        Raises:
            TranslationError: If translation fails
        """
        try:
            messages = self._build_messages(chinese_text)
            logger.info(f"Sending translation request for text length: {len(chinese_text)}")

            response = await llm_client.chat(messages)
            logger.debug(f"LLM response received: {response.content[:200]}...")

            translation, keywords = self._parse_response(response.content)
            logger.info(
                f"Translation successful. Keywords count: {len(keywords)}"
            )

            return translation, keywords

        except TranslationError:
            raise
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise TranslationError(f"Translation service error: {str(e)}")


# Global translator instance
translator = Translator()
