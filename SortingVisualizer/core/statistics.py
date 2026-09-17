import time


class Statistics:

    def __init__(self):
        """Khởi tạo Statistics."""
        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0
        self.end_time = 0
        self.is_running = False  # Đang đếm giờ (chưa stop_timer)

    def add_comparison(self):
        """Tăng số lần so sánh."""
        self.comparisons += 1

    def add_swap(self):
        """Tăng số lần hoán đổi."""
        self.swaps += 1

    def start_timer(self):
        """Bắt đầu đếm thời gian."""
        self.start_time = time.time()
        self.end_time = self.start_time  # tránh dính end_time cũ của lần chạy trước
        self.is_running = True

    def stop_timer(self):
        """Kết thúc đếm thời gian."""
        self.end_time = time.time()
        self.is_running = False

    def get_execution_time(self):
        if self.is_running:
            return time.time() - self.start_time
        return self.end_time - self.start_time

    def reset(self):
        """Đặt lại thống kê."""
        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0
        self.end_time = 0
        self.is_running = False

    def get_stats(self):
        return {
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'execution_time': self.get_execution_time()
        }

    def __str__(self):
        return (f"Comparisons: {self.comparisons}, "
                f"Swaps: {self.swaps}, "
                f"Time: {self.get_execution_time():.3f}s")