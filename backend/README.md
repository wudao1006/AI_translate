# AI Translation Assistant - Backend

Python FastAPI backend for AI-powered Chinese to English translation with keyword extraction.

## Features

- Translate Chinese text to English using LLM
- Extract 3-5 keywords from input text
- Multi-provider support: OpenAI, Claude, DeepSeek, Qwen, Moonshot (Kimi)
- Uses official SDKs: OpenAI SDK and Anthropic SDK
- Structured logging with request tracking
- Input validation and error handling

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

3. Run the server:
```bash
python app.py
# or
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /api/translate

Translate Chinese text to English and extract keywords.

**Request:**
```json
{
  "text": "你好,欢迎使用翻译助手。"
}
```

**Response:**
```json
{
  "translation": "Hello, welcome to the translation assistant.",
  "keywords": ["welcome", "translation", "assistant"]
}
```

**Error Response:**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```

## Configuration

All configuration is via environment variables (see `.env.example`):

- `LLM_PROVIDER`: Provider to use (openai, claude, deepseek, qwen)
- `LLM_API_KEY`: Your API key for the selected provider
- `LLM_MODEL`: Model identifier
- `LLM_TIMEOUT`: Request timeout in seconds
- `LLM_BASE_URL`: Optional custom base URL for compatible providers
- `MAX_TEXT_LENGTH`: Maximum input text length
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Project Structure

```
backend/
├── app.py                 # FastAPI application entry
├── config.py              # Configuration management
├── api/
│   └── translate.py       # Translation endpoint
├── models/
│   └── schemas.py         # Pydantic models
├── services/
│   ├── translator.py      # Translation service
│   └── llm_client.py      # LLM provider clients
└── utils/
    └── logging.py         # Logging utilities
```

## Provider-Specific Notes

### OpenAI
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-3.5-turbo
```

### Claude (Anthropic)
```env
LLM_PROVIDER=claude
LLM_API_KEY=sk-ant-...
LLM_MODEL=claude-3-haiku-20240307
```

### DeepSeek
```env
LLM_PROVIDER=deepseek
LLM_API_KEY=sk-...
LLM_MODEL=deepseek-chat
```

### Qwen (Tongyi Qianwen)
```env
LLM_PROVIDER=qwen
LLM_API_KEY=sk-...
LLM_MODEL=qwen-turbo
```

### Moonshot (Kimi) - OpenAI-compatible
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=moonshot-v1-8k
LLM_BASE_URL=https://api.moonshot.cn/v1
```

### Other OpenAI-compatible APIs
Any OpenAI-compatible API can be used by setting `LLM_BASE_URL`:
```env
LLM_PROVIDER=openai
LLM_API_KEY=your-api-key
LLM_MODEL=model-name
LLM_BASE_URL=https://your-api-endpoint.com/v1
```
