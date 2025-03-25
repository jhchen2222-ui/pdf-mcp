# PDF MCP 服务


## 系统要求

- 软件：Python 3.10+

## 快速开始

1. 克隆仓库并进入目录：
   ```bash
   git clone https://github.com/jhchen2222-ui/pdf-mcp.git
   cd pdf-mcp
   ```

2. 创建虚拟环境并安装依赖：
   
   **Linux/macOS**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   ```
   
   **Windows**:
   ```bash
   uv venv
   .venv\Scripts\activate
   uv pip install -e .
   ```
3. 启动服务：
   ```bash
   uv run main.py
   ```

## Cline 配置

在Cline中添加以下配置：

**Windows**:
```json
{
    "mcpServers": {
        "pdfmcp": {
            "command": "uv",
            "args": [
                "--directory",
                "C:\\path\\to\\pdf-mcp",
                "run",
                "main.py"
            ]
        }
    }
}
```

**Linux/macOS**:
```json
{
    "mcpServers": {
        "pdfmcp": {
            "command": "uv",
            "args": [
                "--directory",
                "/path/to/pdf-mcp",
                "run",
                "main.py"
            ]
        }
    }
}
```
