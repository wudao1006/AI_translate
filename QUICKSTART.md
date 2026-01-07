# 快速开始指南

## 项目概览

AI翻译助手 - 一个完整的中英文翻译应用，包含：
- **后端**: Python FastAPI + 多LLM支持
- **前端**: Flutter跨平台移动应用

## 文件结构

```
ai-translation-assistant/
├── backend/                    # Python后端
│   ├── app.py                 # 主应用
│   ├── config.py              # 配置
│   ├── requirements.txt       # 依赖
│   ├── .env.example          # 配置模板
│   ├── api/                  # API路由
│   ├── models/               # 数据模型
│   ├── services/             # 业务逻辑
│   └── utils/                # 工具函数
│
├── flutter_app/              # Flutter前端
│   ├── lib/
│   │   ├── main.dart        # 应用入口
│   │   ├── screens/         # 界面
│   │   ├── services/        # API客户端
│   │   └── models/          # 数据模型
│   └── pubspec.yaml         # 依赖配置
│
├── README.md                 # 项目文档
├── API_TESTING.md           # API测试指南
├── start.bat                # Windows启动脚本
└── start.sh                 # Linux/Mac启动脚本
```

## 第一步：后端设置

### 1.1 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

### 1.2 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件
notepad .env  # Windows
# 或
nano .env     # Linux/Mac
```

**必须配置的项目：**
```env
LLM_PROVIDER=openai          # 选择: openai | claude | deepseek | qwen
LLM_API_KEY=your_api_key     # 你的API密钥
LLM_MODEL=gpt-3.5-turbo      # 模型名称
```

### 1.3 启动后端服务

```bash
python app.py
```

后端将运行在: `http://localhost:8000`

**验证后端运行：**
```bash
curl http://localhost:8000/health
```

应返回: `{"status": "healthy"}`

## 第二步：前端设置

### 2.1 安装Flutter依赖

```bash
cd flutter_app
flutter pub get
```

### 2.2 配置API地址

编辑 `lib/main.dart`，修改第15行的API地址：

```dart
final apiClient = ApiClient(
  baseUrl: 'http://localhost:8000',  // 根据你的环境修改
);
```

**不同设备的配置：**
- **Android模拟器**: `http://10.0.2.2:8000`
- **iOS模拟器**: `http://localhost:8000`
- **真机**: `http://YOUR_LOCAL_IP:8000` (如 `http://192.168.1.100:8000`)

### 2.3 启用Flutter平台支持

首次运行需要启用对应平台：

```bash
# 启用Web支持（推荐，最快）
flutter create . --platforms=web

# 或启用Windows桌面支持
flutter create . --platforms=windows

# 或启用所有平台
flutter create . --platforms=web,windows,android,ios
```

### 2.4 运行Flutter应用

**Web浏览器（推荐）:**
```bash
flutter run -d chrome
```

**Windows桌面:**
```bash
flutter run -d windows
```

**如有Android模拟器:**
```bash
flutter run
# 然后选择你的设备
```

## 第三步：测试应用

### 测试后端API

```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，欢迎使用AI翻译助手"}'
```

**预期返回：**
```json
{
  "translation": "Hello, welcome to use the AI translation assistant",
  "keywords": ["welcome", "AI", "translation", "assistant"]
}
```

### 测试Flutter应用

1. 在应用中输入中文文本
2. 点击"翻译"按钮
3. 查看翻译结果和关键词

## 后端快速启动脚本

### Windows
双击运行 `start.bat` 或在命令行执行：
```cmd
start.bat
```

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

## 常见问题

### 1. 后端启动失败

**检查项：**
- ✅ Python版本 >= 3.10
- ✅ 已安装所有依赖 (`pip install -r requirements.txt`)
- ✅ `.env` 文件存在且配置正确
- ✅ API密钥有效

### 2. Flutter提示"No supported devices"

这是因为Flutter项目还没有启用对应平台支持。

**解决方法：**
```bash
cd flutter_app
# 启用Web支持（推荐）
flutter create . --platforms=web
# 然后运行
flutter run -d chrome
```

更多详情见: [flutter_app/PLATFORM_SETUP.md](flutter_app/PLATFORM_SETUP.md)

### 3. Flutter无法连接后端

**检查项：**
- ✅ 后端已启动并运行在 http://localhost:8000
- ✅ `lib/main.dart` 中的 baseUrl 配置正确
- ✅ 如使用真机，确保手机和电脑在同一网络
- ✅ 防火墙允许8000端口访问

### 4. LLM API调用失败

**检查项：**
- ✅ API密钥正确
- ✅ 网络连接正常
- ✅ API额度充足
- ✅ 模型名称正确

## 支持的LLM提供商

### OpenAI
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-3.5-turbo
```

### Claude
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

### 通义千问 (Qwen)
```env
LLM_PROVIDER=qwen
LLM_API_KEY=sk-...
LLM_MODEL=qwen-turbo
```

### Moonshot (Kimi)
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=moonshot-v1-8k
LLM_BASE_URL=https://api.moonshot.cn/v1
```

## 下一步

1. 📖 查看完整文档: [README.md](README.md)
2. 🧪 API测试指南: [API_TESTING.md](API_TESTING.md)
3. 🔧 后端详细说明: [backend/README.md](backend/README.md)
4. 📱 Flutter应用说明: [flutter_app/README.md](flutter_app/README.md)

## 获取帮助

如遇到问题，请检查：
1. 后端日志（控制台输出）
2. Flutter日志（`flutter run` 输出）
3. 浏览器开发者工具（如使用Web版）
4. API文档: http://localhost:8000/docs

## 开发建议

- 使用 `uvicorn app:app --reload` 启动后端以支持热重载
- 使用 VS Code + Flutter插件获得最佳开发体验
- 建议使用虚拟环境运行Python后端
- 定期检查API使用量和成本

祝使用愉快！ 🎉
