# Agent-Study

## 🌟 项目简介

这是一个基于 [hello-agents](https://github.com/datawhalechina/hello-agents/) 的学习项目，旨在通过构建一个简单的智能助手（Travel Agent）来理解 Agent 的核心概念和工作流。


## 📦 安装指南

1. **克隆项目**
   ```bash
   git clone https://github.com/RodePachi/agent-study.git
   cd agent-study
   ```

2. **初始化环境**
   项目使用 [Hatch](https://hatch.pypa.io/) 进行管理。你可以通过 `Makefile` 快速初始化：
   ```bash
   make init
   ```
   这会创建一个默认的虚拟环境并安装所有依赖。

3. **配置环境变量**
   在项目根目录下创建一个 `env/.env` 文件，并填写以下配置：
   ```ini
   API_KEY=your_openai_api_key
   BASE_URL=your_openai_base_url
   MODEL_ID=your_model_id
   TAVILY_API_KEY=your_tavily_api_key
   ```

## 🎮 使用方法

### 运行 Agent
进入 Hatch 环境并运行主程序：
```bash
hatch shell
python src/agent/travel/travel_agent.py
```
默认情况下，Agent 会查询“东京”的天气并推荐景点。你可以修改 `travel_agent.py` 中的 `main()` 函数调用来测试不同的城市。

### 运行测试
使用 `Makefile` 运行测试：
```bash
make test
```

## 📂 项目结构

```text
.
├── docs/               # 项目文档
├── env/                # 环境变量配置文件 (建议在此存放 .env)
├── src/
│   └── agent/
│       ├── travel/     # Travel Agent 核心逻辑
│       │   └── travel_agent.py
│       └── resource/   # 资源文件
│           └── prompt/ # 系统提示词模版
├── tests/              # 测试脚本
├── Makefile            # 快捷命令
├── pyproject.toml      # 项目配置文件
└── README.md           # 项目说明文档
```

## 📚 致谢

感谢 [Datawhale](https://github.com/datawhalechina) 提供的 [hello-agents](https://github.com/datawhalechina/hello-agents/) 教程，为本项目提供了很好的学习资源。
