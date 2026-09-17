import pygame
from abc import ABC, abstractmethod
from core.statistics import Statistics
from visualization.colors import Colors


class SortingAlgorithm(ABC):

    def __init__(self, array_data, visualizer, app=None):
        self.array_data = array_data
        self.visualizer = visualizer
        self.app = app
        self.statistics = Statistics()
        self.is_running = False
        self.is_paused = False
        self.speed = 50  # Tốc độ (1-100)

    @abstractmethod
    def sort(self):
        """
        Phương thức sắp xếp (bắt buộc phải implement).
        Sẽ được override bởi các lớp con.
        """
        pass

    def set_speed(self, speed):
        self.speed = max(1, min(100, speed))

    def reset_statistics(self):
        """Đặt lại thống kê."""
        self.statistics.reset()

    def get_statistics(self):
        return self.statistics

    def pause(self):
        """Tạm dừng sắp xếp."""
        self.is_paused = True

    def resume(self):
        """Tiếp tục sắp xếp."""
        self.is_paused = False

    def stop(self):
        """Dừng sắp xếp."""
        self.is_running = False

    def _tick(self, delay_ms):
        """
        Vẽ lại màn hình và xử lý sự kiện hệ thống trong lúc sort,
        để chương trình không bị đơ (Not Responding).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                pygame.quit()
                import sys
                sys.exit()
            elif self.app is not None:
                # Chuyển sự kiện cho Application để Pause/Resume/Reset và các
                # slider/dropdown vẫn hoạt động bình thường trong lúc đang sort.
                self.app.handle_sorting_event(event)

        if self.app is not None:
            self.app.draw()
        else:
            screen = self.visualizer.screen
            screen.fill(Colors.BACKGROUND)
            self.visualizer.draw()
            pygame.display.flip()

        pygame.time.delay(delay_ms)

        if self.is_paused:
            self._wait_if_paused()

    def _wait_if_paused(self):
        while self.is_paused and self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()
                    import sys
                    sys.exit()
                elif self.app is not None:
                    self.app.handle_sorting_event(event)

            if self.app is not None:
                self.app.draw()

            pygame.time.delay(30)

    def __str__(self):
        return self.__class__.__name__