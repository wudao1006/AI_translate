# API测试示例

本文件包含API测试示例，可以使用curl或任何HTTP客户端测试。

## 1. 健康检查

```bash
curl http://localhost:8000/health
```

**响应:**
```json
{
  "status": "healthy"
}
```

## 2. 翻译请求

### 基本示例

```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，欢迎使用AI翻译助手。这是一个功能强大的翻译工具。"}'
```

**预期响应:**
```json
{
  "translation": "Hello, welcome to use the AI translation assistant. This is a powerful translation tool.",
  "keywords": ["AI", "translation", "assistant", "tool", "powerful"]
}
```

### 更多示例

#### 示例1: 技术文档
```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "FastAPI是一个现代、快速的Web框架，用于构建API。它基于Python类型提示，提供自动API文档生成功能。"}'
```

#### 示例2: 日常对话
```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "今天天气真不错，我们一起去公园散步吧。"}'
```

#### 示例3: 商务邮件
```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "尊敬的客户，感谢您对我们产品的关注。我们将在三个工作日内回复您的询问。"}'
```

## 3. 错误测试

### 空文本
```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

**预期响应:** 422 或 400 错误

### 超长文本
```bash
# 生成一个超过4000字符的文本
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$(python -c 'print("测试" * 2000)')\"}"
```

**预期响应:** 400 错误

## 4. 使用Python测试

```python
import requests

url = "http://localhost:8000/api/translate"
data = {
    "text": "人工智能正在改变世界，深度学习和神经网络是其核心技术。"
}

response = requests.post(url, json=data)
result = response.json()

print("翻译结果:", result["translation"])
print("关键词:", ", ".join(result["keywords"]))
```

## 5. 使用JavaScript测试

```javascript
const url = "http://localhost:8000/api/translate";
const data = {
  text: "机器学习是人工智能的一个重要分支，它使计算机能够从数据中学习。"
};

fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(data),
})
  .then(response => response.json())
  .then(result => {
    console.log("翻译结果:", result.translation);
    console.log("关键词:", result.keywords);
  })
  .catch(error => console.error("错误:", error));
```

## 6. Postman导入

你可以在Postman中创建一个新请求:

- **Method**: POST
- **URL**: `http://localhost:8000/api/translate`
- **Headers**:
  - `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "text": "你好，世界！"
}
```

## 7. 性能测试

使用Apache Bench进行性能测试:

```bash
# 发送100个请求，并发数为10
ab -n 100 -c 10 -p request.json -T application/json http://localhost:8000/api/translate
```

其中 `request.json` 文件内容:
```json
{"text": "这是一个性能测试请求。"}
```
