"""XD Financial Reports 主入口模块.

启动方式:
    cd xd-financial-reports
    python -m xd_financial_reports                  # 默认端口 8000
    python -m xd_financial_reports --port 8080      # 指定端口
    python -m xd_financial_reports --reload         # 开发模式自动重载
"""
import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

# 确保 src 目录在 sys.path 中（支持从项目根目录直接运行）
_SRC_DIR = str(Path(__file__).resolve().parent.parent)
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)


def main(args: Optional[List[str]] = None) -> int:
    """启动 FastAPI HTTP 服务器."""
    parser = argparse.ArgumentParser(
        description="XD Financial Reports API Server",
    )
    parser.add_argument(
        "--host", default="127.0.0.1", help="监听地址 (默认: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=8001, help="监听端口 (默认: 8001)"
    )
    parser.add_argument(
        "--reload", action="store_true", help="开发模式, 文件变更自动重载"
    )
    parsed = parser.parse_args(args)

    import uvicorn

    uvicorn.run(
        "xd_financial_reports.api.app:app",
        host=parsed.host,
        port=parsed.port,
        reload=parsed.reload,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())