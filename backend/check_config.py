"""
Configuration diagnostic script.
Run this to verify your .env configuration is correct.
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

try:
    from config import settings

    print("=" * 60)
    print("Configuration Diagnostic Report")
    print("=" * 60)
    print()

    print("✓ Configuration loaded successfully!")
    print()

    print("Current Settings:")
    print("-" * 60)
    print(f"LLM Provider:  {settings.llm_provider}")
    print(f"LLM Model:     {settings.llm_model}")
    print(f"LLM Timeout:   {settings.llm_timeout}s")

    # Mask API key for security
    api_key = settings.llm_api_key
    if api_key:
        masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
        print(f"LLM API Key:   {masked_key} (length: {len(api_key)})")
    else:
        print(f"LLM API Key:   [NOT SET] ❌")

    if settings.llm_base_url:
        print(f"LLM Base URL:  {settings.llm_base_url}")
    else:
        print(f"LLM Base URL:  [Using default]")

    print()
    print(f"Max Text Len:  {settings.max_text_length}")
    print(f"CORS Origins:  {settings.cors_origins}")
    print(f"Log Level:     {settings.log_level}")
    print()

    # Validation checks
    print("Validation Checks:")
    print("-" * 60)

    issues = []

    if not settings.llm_api_key or settings.llm_api_key.strip() == "":
        issues.append("❌ LLM_API_KEY is empty or not set!")
    else:
        print("✓ API key is configured")

    if settings.llm_provider not in ["openai", "claude", "deepseek", "qwen"]:
        issues.append(f"❌ Invalid LLM provider: {settings.llm_provider}")
    else:
        print(f"✓ Valid LLM provider: {settings.llm_provider}")

    if settings.llm_base_url:
        if not settings.llm_base_url.startswith(("http://", "https://")):
            issues.append(f"❌ Invalid base URL format: {settings.llm_base_url}")
        else:
            print(f"✓ Custom base URL is valid")

    print()

    if issues:
        print("Issues Found:")
        print("-" * 60)
        for issue in issues:
            print(issue)
        print()
        print("Please fix the issues in your .env file and try again.")
        sys.exit(1)
    else:
        print("=" * 60)
        print("✓ All checks passed! Configuration is valid.")
        print("=" * 60)
        print()
        print("You can now start the backend server:")
        print("  python app.py")

except ValueError as e:
    print("=" * 60)
    print("Configuration Error")
    print("=" * 60)
    print()
    print(f"❌ {str(e)}")
    print()
    print("Please check your .env file and make sure all required")
    print("configuration values are set correctly.")
    print()
    print("Example .env configuration:")
    print("-" * 60)
    print("LLM_PROVIDER=openai")
    print("LLM_API_KEY=sk-your-api-key-here")
    print("LLM_MODEL=gpt-3.5-turbo")
    print("LLM_TIMEOUT=30")
    print("LLM_BASE_URL=")
    print()
    sys.exit(1)

except Exception as e:
    print("=" * 60)
    print("Unexpected Error")
    print("=" * 60)
    print()
    print(f"❌ {type(e).__name__}: {str(e)}")
    print()
    import traceback
    traceback.print_exc()
    sys.exit(1)
