# Flutter平台配置说明

## 问题：没有支持的设备

如果运行 `flutter run` 时看到 "No supported devices connected" 错误，说明Flutter项目需要启用对应的平台支持。

## 解决方案

### 方法1: 启用Web支持（推荐用于快速测试）

```bash
cd flutter_app
flutter create . --platforms=web
flutter run -d chrome
```

### 方法2: 启用Windows桌面支持

```bash
cd flutter_app
flutter create . --platforms=windows
flutter run -d windows
```

### 方法3: 启用所有平台

```bash
cd flutter_app
flutter create . --platforms=web,windows,android,ios
```

## 运行应用

### 在Web浏览器中运行
```bash
cd flutter_app
flutter run -d chrome
# 或
flutter run -d edge
```

### 在Windows桌面运行
```bash
cd flutter_app
flutter run -d windows
```

### 在Android模拟器运行
```bash
# 先启动Android模拟器
cd flutter_app
flutter run -d emulator-5554
```

### 在iOS模拟器运行（仅Mac）
```bash
cd flutter_app
flutter run -d "iPhone 15"
```

## 配置API地址

### Web和Windows桌面
使用 `http://localhost:8000`（后端在同一台电脑）

### Android模拟器
使用 `http://10.0.2.2:8000`

### iOS模拟器
使用 `http://localhost:8000`

### 真机设备
使用 `http://YOUR_LOCAL_IP:8000`（如 `http://192.168.1.100:8000`）

查找本机IP:
- Windows: `ipconfig` 查看 IPv4 地址
- Mac/Linux: `ifconfig` 或 `ip addr`

## 验证Flutter安装

```bash
flutter doctor
```

确保所有需要的组件都已安装。

## 常见问题

### 1. Flutter命令未找到
确保Flutter SDK已添加到系统PATH环境变量。

### 2. Chrome/Edge启动失败
确保已安装Chrome或Edge浏览器。

### 3. Windows桌面应用启动失败
确保已安装Visual Studio 2022（包含"使用C++的桌面开发"工作负载）。

### 4. CORS错误（Web平台）
后端已配置CORS允许所有来源，应该不会有问题。如有问题，检查 [backend/config.py](../backend/config.py) 中的 `cors_origins` 设置。
