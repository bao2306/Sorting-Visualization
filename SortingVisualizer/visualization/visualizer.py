"""
Vẽ mảng lên màn hình dưới dạng biểu đồ cột.
"""

import pygame
from visualization.colors import Colors


class Visualizer:
    """
    Vẽ dữ liệu mảng dưới dạng bar chart.
    Các trạng thái: default, comparing, swapping, sorted, pivot, merged
    """

    def __init__(self, screen, array_data, width=1200, height=600):
        """
        Khởi tạo Visualizer.

        Args:
            screen: Pygame screen object
            array_data (list): Mảng dữ liệu
            width (int): Chiều rộng vùng vẽ
            height (int): Chiều cao vùng vẽ
        """
        self.screen = screen
        self.array_data = array_data
        self.width = width
        self.height = height
        self.bar_width = width / len(array_data)
        self.max_value = max(array_data) if array_data else 500

        # Lưu trạng thái của từng phần tử
        self.states = ['default'] * len(array_data)
        self.padding = 50  # Khoảng cách từ mép màn hình

    def update_array(self, array_data):
        self.array_data = array_data
        self.max_value = max(array_data) if array_data else 500
        self.bar_width = self.width / len(array_data)

    def set_state(self, index, state):
        if 0 <= index < len(self.states):
            self.states[index] = state

    def set_states(self, indices, state):
        """
        Thiết lập trạng thái cho nhiều phần tử.

        Args:
            indices (list): Danh sách chỉ số
            state (str): Trạng thái
        """
        for idx in indices:
            self.set_state(idx, state)

    def reset_states(self):
        """Đặt lại tất cả trạng thái về default."""
        self.states = ['default'] * len(self.array_data)

    def draw_bar(self, x, y, width, height, state):
        color = Colors.get_color_by_state(state)
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        pygame.draw.rect(self.screen, Colors.BLACK, (x, y, width, height), 1)

    def draw_array(self):
        """Vẽ toàn bộ mảng."""
        x_offset = self.padding
        y_base = self.height + self.padding

        gap = min(2.0, self.bar_width * 0.3)
        bar_draw_width = max(1.0, self.bar_width - gap)

        for i, value in enumerate(self.array_data):
            # Tính chiều cao cột
            bar_height = (value / self.max_value) * (self.height - 50)
            x = x_offset + i * self.bar_width
            y = y_base - bar_height

            # Vẽ cột
            self.draw_bar(x, y, bar_draw_width, bar_height, self.states[i])

    def draw(self):
        """Vẽ toàn bộ visualization."""
        self.draw_array()