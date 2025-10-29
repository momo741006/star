#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel Serverless Function Entry Point
虹靈御所占星主角生成系統 - Vercel 適配版
"""

import sys
import os

# 添加父目錄到 Python 路徑，以便導入 main.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 導入 Flask app
from main import app

# Vercel 使用這個作為 WSGI 應用入口
# Vercel 的 Python runtime 會自動查找名為 'app' 或 'application' 的 WSGI 應用
application = app

# 本地測試支援
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

