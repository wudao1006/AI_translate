# AI翻译助手 - 设计方案

## 范围
构建一个简单的AI翻译助手，包含：
- 后端API：POST /translate
- Flutter界面：输入框、翻译按钮、结果展示区

## 目标
- 将中文翻译为英文，使用任意大模型API。
- 返回输入内容的关键词列表（3-5个）。
- 实现尽量简洁，同时具备基本的配置、错误处理和日志能力。

## 非目标
- 用户账户、历史记录、数据存储或分析。
- 复杂的UI/UX设计。
- 离线翻译能力。

## 架构概览
- 后端：Python + FastAPI，单一接口。
- 大模型：通过配置选择OpenAI/Claude/DeepSeek/通义千问等。
- 前端：Flutter调用后端API。

数据流：
1) Flutter发送POST /translate请求。
2) 后端校验输入，调用大模型，返回翻译结果与关键词。
3) Flutter渲染结果或错误。

## 后端设计（FastAPI）

### 接口
- POST /translate
- 请求JSON：{ "text": "<中文内容>" }
- 返回JSON：{ "translation": "<英文>", "keywords": ["k1", "k2", "k3"] }

### 模块划分
- app.py
  - FastAPI应用初始化、路由注册、CORS配置。
- api/translate.py
  - 处理请求、校验、组装响应。
- models/schemas.py
  - Pydantic模型：TranslateRequest、TranslateResponse、ErrorResponse。
- services/translator.py
  - 核心业务：构建提示词、调用LLM、解析输出。
- services/llm_client.py
  - 统一LLM接口与各厂商适配器。
- config.py
  - 环境变量配置（provider、API key、model、timeout）。
- utils/logging.py
  - 日志与请求耗时记录。

### LLM交互
- 使用单次提示词，请求返回严格JSON：
  - “将中文翻译成英文，并提取3-5个关键词。只返回JSON，字段为translation与keywords。”
- 解析JSON，必要时重试一次（可选）。

### 校验与限制
- text字段必填，去除首尾空白。
- 限制长度（如2-4k字符）避免过长提示。
- 输入错误返回400；LLM调用失败返回502/503。

### 配置项
- 环境变量：
  - LLM_PROVIDER: openai | claude | deepseek | qwen
  - LLM_API_KEY
  - LLM_MODEL
  - LLM_TIMEOUT

### 错误处理
- 统一错误格式：{ "error": { "code": "...", "message": "..." } }
- 服务端记录详细错误，客户端返回简洁提示。

## Flutter界面设计

### 界面布局
- 顶部标题："AI翻译助手"。
- 输入区域：多行TextField，输入中文。
- 按钮："翻译"。
- 结果区域：
  - 英文翻译文本。
  - 关键词展示（Chip或逗号分隔）。
- 状态提示：加载中、错误提示。

### 状态模型
- Idle：无结果。
- Loading：按钮不可用，显示加载动画。
- Success：展示翻译结果与关键词。
- Error：展示错误提示，可重试。

### Flutter结构
- lib/main.dart
  - 应用入口，主题配置。
- lib/screens/translate_screen.dart
  - 界面与状态逻辑。
- lib/services/api_client.dart
  - HTTP调用 /translate。
- lib/models/translate_result.dart
  - 响应模型解析。

## API示例
请求：
{ "text": "你好，欢迎使用翻译助手。" }

返回：
{ "translation": "Hello, welcome to the translation assistant.",
  "keywords": ["welcome", "translation", "assistant"] }

## 测试（可选）
- 后端：
  - 请求校验测试。
  - LLM输出解析测试。
- Flutter：
  - 加载/成功/失败状态的Widget测试。

## 部署说明
- 后端：uvicorn启动，配置LLM环境变量。
- Flutter：配置后端Base URL（开发/生产）。
