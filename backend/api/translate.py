"""
Translation API endpoint.
Handles POST /translate requests with validation and error handling.
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from models.schemas import TranslateRequest, TranslateResponse, ErrorResponse, ErrorDetail
from services.translator import translator, TranslationError
from config import settings
from utils.logging import get_logger, set_request_id, Timer

logger = get_logger(__name__)

router = APIRouter()


@router.post(
    "/translate",
    response_model=TranslateResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        502: {"model": ErrorResponse, "description": "LLM service error"},
        503: {"model": ErrorResponse, "description": "Service unavailable"},
    },
)
async def translate(request: TranslateRequest):
    """
    Translate Chinese text to English and extract keywords.

    Args:
        request: TranslateRequest with text field

    Returns:
        TranslateResponse with translation and keywords

    Raises:
        HTTPException: On validation or service errors
    """
    req_id = set_request_id()
    logger.info(f"Translation request received. Text length: {len(request.text)}")

    # Validate text length
    if len(request.text) > settings.max_text_length:
        logger.warning(f"Text too long: {len(request.text)} chars")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "TEXT_TOO_LONG",
                    "message": f"Text exceeds maximum length of {settings.max_text_length} characters",
                }
            },
        )

    try:
        with Timer() as timer:
            translation, keywords = await translator.translate(request.text)

        logger.info(f"Translation completed in {timer.elapsed:.2f}s")

        return TranslateResponse(translation=translation, keywords=keywords)

    except TranslationError as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": {
                    "code": "TRANSLATION_FAILED",
                    "message": "Failed to translate text. Please try again.",
                }
            },
        )
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": {
                    "code": "SERVICE_ERROR",
                    "message": "Translation service is temporarily unavailable",
                }
            },
        )
