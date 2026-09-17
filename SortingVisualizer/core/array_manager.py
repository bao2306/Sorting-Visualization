import random


class ArrayManager:

    def __init__(self, size=50):
        """
        Khởi tạo ArrayManager.
        """
        self.size = size
        self.data = []
        self.original_data = []
        self.generate()

    def generate(self):
        self.data = [random.randint(10, 500) for _ in range(self.size)]
        self.original_data = self.data.copy()

    def reset(self):
        """Đặt lại mảng về trạng thái gốc."""
        self.data = self.original_data.copy()

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data.copy()
        self.original_data = self.data.copy()

    def set_size(self, size):
        self.size = size
        self.generate()

    def get_size(self):
        return self.size

    def __str__(self):
        return f"ArrayManager(size={self.size})"

import random

