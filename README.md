# XD Financial Reports

XD Financial Reports - 金融报表处理工具

## 项目结构

```
xd-financial-reports/
├── src/
│   └── xd_financial_reports/
│       ├── __init__.py
│       └── __main__.py
├── pyproject.toml
├── requirements.txt
├── .gitignore
└── README.md
```

## 环境要求

- Python >= 3.10

## 快速开始

### 创建虚拟环境

```bash
python -m venv .venv
```

### 激活虚拟环境

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 安装依赖

```bash
pip install -e .
```

安装开发依赖：

```bash
pip install -e ".[dev]"
```

### 运行

```bash
xd-financial-reports
```

或直接使用 Python：

```bash
python -m xd_financial_reports
```

## 开发

### 代码格式化

```bash
black src/
isort src/
```

### 代码检查

```bash
ruff check src/
mypy src/
```

### 运行测试

```bash
pytest
```

## 许可证

MIT