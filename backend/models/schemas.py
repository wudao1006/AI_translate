"""
Pydantic models for request/response validation and serialization.
"""
from pydantic import BaseModel, Field, field_validator


class TranslateRequest(BaseModel):
    """Request model for translation endpoint."""

    text: str = Field(..., min_length=1, description="Chinese text to translate")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Validate and clean text input."""
        v = v.strip()
        if not v:
            raise ValueError("Text cannot be empty or whitespace only")
        return v


class TranslateResponse(BaseModel):
    """Response model for successful translation."""

    translation: str = Field(..., description="English translation")
    keywords: list[str] = Field(
        ..., min_length=3, max_length=5, description="3-5 extracted keywords"
    )


class ErrorDetail(BaseModel):
    """Error detail structure."""

    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")


class ErrorResponse(BaseModel):
    """Error response model."""

    error: ErrorDetail
