"""
Điểm vào (Entry Point) của chương trình.
Chạy file này để khởi động ứng dụng.
"""

import sys
import os

# Thêm thư mục hiện tại vào sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import pygame trước tiên
import pygame

from core.application import Application


def main():
    """Hàm chính."""
    app = Application(width=1400, height=800)
    app.run()


if __name__ == "__main__":
    main()