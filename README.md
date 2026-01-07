# AI Translation Assistant

一个完整的AI翻译助手应用，包含Python FastAPI后端和Flutter移动端。使用大模型API将中文翻译为英文，并提取关键词。

## 项目结构

```
.
├── backend/                 # Python FastAPI后端
│   ├── app.py              # 应用入口
│   ├── config.py           # 配置管理
│   ├── api/                # API路由
│   ├── models/             # 数据模型
│   ├── services/           # 业务逻辑
│   ├── utils/              # 工具函数
│   └── requirements.txt    # Python依赖
│
├── flutter_app/            # Flutter移动应用
│   ├── lib/
│   │   ├── main.dart       # 应用入口
│   │   ├── screens/        # 界面
│   │   ├── services/       # API客户端
│   │   └── models/         # 数据模型
│   └── pubspec.yaml        # Flutter依赖
│
└── ai_translation_assistant_design.md  # 设计文档
```

## 功能特性

### 后端 (FastAPI)
- ✅ RESTful API接口 (POST /api/translate)
- ✅ 多LLM提供商支持:
  - OpenAI (gpt-3.5-turbo, gpt-4, etc.)
  - Anthropic Claude
  - DeepSeek
  - 阿里通义千问 (Qwen)
- ✅ 结构化日志与请求追踪
- ✅ 输入验证与错误处理
- ✅ CORS配置
- ✅ 配置文件管理

### 前端 (Flutter)
- ✅ 简洁的Material Design界面
- ✅ 实时翻译功能
- ✅ 关键词提取展示
- ✅ 加载状态指示
- ✅ 错误处理与提示
- ✅ 跨平台支持 (Android/iOS/Web)

## 快速开始

### 1. 后端设置

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，设置你的API密钥

# 启动服务
python app.py
```

后端将在 `http://localhost:8000` 启动

访问API文档: `http://localhost:8000/docs`

### 2. 前端设置

```bash
# 进入Flutter应用目录
cd flutter_app

# 安装依赖
flutter pub get

# 配置API地址
# 编辑 lib/main.dart，设置正确的baseUrl

# 运行应用
flutter run
```

## 配置说明

### 后端配置 (.env)

```env
# LLM提供商选择
LLM_PROVIDER=openai          # 选项: openai | claude | deepseek | qwen
LLM_API_KEY=your_api_key     # 你的API密钥
LLM_MODEL=gpt-3.5-turbo      # 模型名称
LLM_TIMEOUT=30               # 请求超时(秒)
LLM_BASE_URL=                # 可选的自定义API地址

# API配置
MAX_TEXT_LENGTH=4000         # 最大输入长度
LOG_LEVEL=INFO              # 日志级别
```

### 前端配置

编辑 [flutter_app/lib/main.dart](flutter_app/lib/main.dart)，设置API地址:

```dart
final apiClient = ApiClient(
  baseUrl: 'http://localhost:8000',  // 修改为你的后端地址
);
```

**不同环境的配置:**
- **Android模拟器**: `http://10.0.2.2:8000`
- **iOS模拟器**: `http://localhost:8000`
- **真机调试**: `http://YOUR_LOCAL_IP:8000`

## API接口

### POST /api/translate

**请求:**
```json
{
  "text": "你好，欢迎使用翻译助手。"
}
```

**响应:**
```json
{
  "translation": "Hello, welcome to the translation assistant.",
  "keywords": ["welcome", "translation", "assistant"]
}
```

**错误响应:**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述"
  }
}
```

## LLM提供商配置

### OpenAI
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-3.5-turbo
```

### Anthropic Claude
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

### 阿里通义千问
```env
LLM_PROVIDER=qwen
LLM_API_KEY=sk-...
LLM_MODEL=qwen-turbo
```

### Moonshot (Kimi) - OpenAI兼容
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=moonshot-v1-8k
LLM_BASE_URL=https://api.moonshot.cn/v1
```

### 其他OpenAI兼容API
任何OpenAI兼容的API都可以通过设置 `LLM_BASE_URL` 使用：
```env
LLM_PROVIDER=openai
LLM_API_KEY=your-api-key
LLM_MODEL=model-name
LLM_BASE_URL=https://your-api-endpoint.com/v1
```

## 开发

### 后端开发

```bash
cd backend

# 开发模式运行（自动重载）
uvicorn app:app --reload

# 查看日志
tail -f logs/app.log
```

### 前端开发

```bash
cd flutter_app

# 运行在特定设备
flutter run -d <device_id>

# 热重载
# 在运行时按 r 键

# 代码格式化
flutter format lib/
```

## 构建发布版本

### 后端部署

```bash
# 使用Gunicorn部署
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Flutter应用构建

```bash
# Android APK
flutter build apk --release

# iOS
flutter build ios --release

# Web
flutter build web --release
```

## 技术栈

### 后端
- Python 3.10+
- FastAPI - Web框架
- Pydantic - 数据验证
- OpenAI SDK - OpenAI API客户端
- Anthropic SDK - Claude API客户端
- uvicorn - ASGI服务器

### 前端
- Flutter 3.0+
- Dart 3.0+
- http package - HTTP客户端

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 作者

AI Translation Assistant Team
