# robot-mcp-server

为大语言模型提供机器人控制能力的MCP服务器

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 功能特性

- ✅ 支持宇树机器人运动控制
- ✅ 支持大疆无人机起飞/降落控制
- ✅ 基于Model Context Protocol (MCP) 的标准接口
- 📡 实时状态监控
- 🛑 紧急停止机制
- 📊 完善的日志记录

## 安装指南

### 前置要求
- Python 3.10+
- 宇树机器人SDK2 (自动安装)
- 大疆Tello无人机SDK (自动安装)

```bash
# 创建并激活虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 安装依赖
pip install git+https://github.com/unitreerobotics/unitree_sdk2_python.git
pip install djitellopy
```

## 快速开始

```python
from modelcontextprotocol import Client

# 连接MCP服务
client = Client.connect_stdio()

# 控制宇树机器人
client.call_tool("unitree_connect", {})
client.call_tool("unitree_move", {"velocity": 1.5})

# 控制大疆无人机
client.call_tool("dji_connect", {})
client.call_tool("dji_takeoff", {"height": 2.0})
```

## API文档

### 宇树机器人工具
- `unitree_connect`: 建立机器人连接
- `unitree_move(velocity: float, duration: float)`: 控制移动
- `unitree_stop()`: 紧急停止

### 大疆无人机工具
- `dji_connect`: 建立无人机连接
- `dji_takeoff(height: float)`: 起飞到指定高度
- `dji_land()`: 安全降落

## 开发指南

项目结构：
```
├── src/
│   ├── main.py          # 主服务入口
│   ├── unitree_adapter.py # 宇树机器人适配器
│   └── dji_adapter.py   # 大疆无人机适配器
├── examples/            # 使用示例
├── requirements.txt     # 依赖列表
└── README.md            # 项目文档
```

## 贡献
欢迎提交Issue和PR，请遵循现有代码风格并添加适当测试。

## 授权协议
[MIT License](LICENSE)

