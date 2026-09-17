import sys
import os

# Fix path để import các module từ folder cha
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from core.array_manager import ArrayManager
from core.statistics import Statistics
from visualization.visualizer import Visualizer
from visualization.colors import Colors
from algorithms.bubble_sort import BubbleSort
from algorithms.quick_sort import QuickSort
from algorithms.merge_sort import MergeSort
from UI.button import Button
from UI.slider import Slider
from UI.dropdown import Dropdown


class Application:
    """
    Lớp chính quản lý toàn bộ ứng dụng.
    Quản lý:
    - Event (chuột, bàn phím)
    - Giao diện (UI)
    - Thuật toán
    - Animation
    """

    def __init__(self, width=1400, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualizer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60

        # Khởi tạo các component
        self.array_manager = ArrayManager(size=100)
        # Giảm chiều cao visualizer còn 580px để chỗ cho UI (buttons, sliders)
        self.visualizer = Visualizer(self.screen, self.array_manager.get_data(), 
                                     width=1200, height=580)

        # Thuật toán
        self.algorithms = {
            'Bubble Sort': BubbleSort(self.array_manager.get_data(), self.visualizer, self),
            'Quick Sort': QuickSort(self.array_manager.get_data(), self.visualizer, self),
            'Merge Sort': MergeSort(self.array_manager.get_data(), self.visualizer, self),
        }
        self.current_algorithm = None
        self.algorithm_name = 'Bubble Sort'

        # Trạng thái
        self.sorting = False
        self.paused = False
        self.last_size = 100  # Lưu kích thước cuối cùng

        # UI Components
        self._init_ui()

    def _init_ui(self):
        """Khởi tạo các thành phần giao diện."""
        button_y = self.height - 80
        button_x_start = 20

        # Buttons
        self.btn_generate = Button(button_x_start, button_y, 100, 50, "Generate")
        self.btn_start = Button(button_x_start + 110, button_y, 100, 50, "Start")
        self.btn_pause = Button(button_x_start + 220, button_y, 100, 50, "Pause")
        self.btn_resume = Button(button_x_start + 330, button_y, 100, 50, "Resume")
        self.btn_reset = Button(button_x_start + 440, button_y, 100, 50, "Reset")

        # Hàng điều khiển phía trên hàng nút, canh trái - cùng hàng với dropdown thuật toán
        control_row_y = button_y - 60

        # Dropdown - Algorithm Selection (đặt đầu tiên, bên trái)
        self.dropdown_algorithm = Dropdown(button_x_start, control_row_y, 150, 30,
                                           list(self.algorithms.keys()))

        # Slider - Array Size Control (10 đến 500 phần tử), nằm ngay bên phải dropdown
        # Chừa đủ khoảng cách để số giá trị (hiển thị bên phải thanh trượt) không bị che khuất
        slider_size_x = self.dropdown_algorithm.rect.right + 70
        self.slider_size = Slider(slider_size_x, control_row_y + 5, 140, 20, 10, 400, 100)

        # Slider - Speed Control (1 đến 100), nằm ngay bên phải slider Size
        slider_speed_x = slider_size_x + 140 + 70
        self.slider_speed = Slider(slider_speed_x, control_row_y + 5, 140, 20, 1, 100, 50)

        # Font cho nhãn
        self.label_font = pygame.font.Font(None, 14)

    def handle_events(self):
        """Xử lý sự kiện (event)."""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Button clicks
                if self.btn_generate.is_clicked(mouse_pos):
                    self.generate_array()
                elif self.btn_start.is_clicked(mouse_pos):
                    self.start_sorting()
                elif self.btn_pause.is_clicked(mouse_pos):
                    self.pause_sorting()
                elif self.btn_resume.is_clicked(mouse_pos):
                    self.resume_sorting()
                elif self.btn_reset.is_clicked(mouse_pos):
                    self.reset()

                # Dropdown click
                self.dropdown_algorithm.is_clicked(mouse_pos)

                # Slider - chỉ bắt đầu kéo khi thực sự bấm chuột trúng thanh trượt
                self.slider_size.start_drag(mouse_pos)
                self.slider_speed.start_drag(mouse_pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.slider_size.on_mouse_release()
                self.slider_speed.on_mouse_release()

            elif event.type == pygame.MOUSEMOTION:
                self.slider_size.update(mouse_pos)
                self.slider_speed.update(mouse_pos)

        self.btn_generate.update(mouse_pos)
        self.btn_start.update(mouse_pos)
        self.btn_pause.update(mouse_pos)
        self.btn_resume.update(mouse_pos)
        self.btn_reset.update(mouse_pos)

        current_size = self.slider_size.get_value()
        if current_size != self.last_size and not self.sorting:
            self.last_size = current_size
            self.array_manager.set_size(current_size)
            self.visualizer.update_array(self.array_manager.get_data())
            self.visualizer.reset_states()

    def handle_sorting_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_pause.is_clicked(mouse_pos):
                self.pause_sorting()
            elif self.btn_resume.is_clicked(mouse_pos):
                self.resume_sorting()
            elif self.btn_reset.is_clicked(mouse_pos):
                if self.current_algorithm:
                    self.current_algorithm.stop()
                self.paused = False
                self.reset()

            # Chỉ cho phép chỉnh Speed trong lúc đang chạy (Size không đổi được khi đang sort)
            self.slider_speed.start_drag(mouse_pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.slider_speed.on_mouse_release()

        elif event.type == pygame.MOUSEMOTION:
            self.slider_speed.update(mouse_pos)
            if self.current_algorithm:
                self.current_algorithm.set_speed(self.slider_speed.get_value())

        self.btn_generate.update(mouse_pos)
        self.btn_start.update(mouse_pos)
        self.btn_pause.update(mouse_pos)
        self.btn_resume.update(mouse_pos)
        self.btn_reset.update(mouse_pos)

    def generate_array(self):
        """Tạo mảng ngẫu nhiên."""
        if not self.sorting:
            self.array_manager.generate()
            self.visualizer.update_array(self.array_manager.get_data())
            self.visualizer.reset_states()

    def start_sorting(self):
        """Bắt đầu sắp xếp."""
        if not self.sorting:
            self.sorting = True
            self.paused = False
            self.visualizer.reset_states()

            # Cập nhật thuật toán được chọn
            self.algorithm_name = self.dropdown_algorithm.get_selected()
            self.current_algorithm = self.algorithms[self.algorithm_name]
            self.current_algorithm.array_data = self.array_manager.get_data()
            self.current_algorithm.set_speed(self.slider_speed.get_value())
            self.current_algorithm.reset_statistics()

            self.current_algorithm.sort()
            self.sorting = False

    def pause_sorting(self):
        """Tạm dừng sắp xếp."""
        if self.sorting and not self.paused:
            self.paused = True
            if self.current_algorithm:
                self.current_algorithm.pause()

    def resume_sorting(self):
        """Tiếp tục sắp xếp."""
        if self.sorting and self.paused:
            self.paused = False
            if self.current_algorithm:
                self.current_algorithm.resume()

    def reset(self):
        """Đặt lại toàn bộ."""
        self.sorting = False
        self.paused = False
        self.array_manager.reset()
        self.visualizer.update_array(self.array_manager.get_data())
        self.visualizer.reset_states()
        if self.current_algorithm:
            self.current_algorithm.reset_statistics()

    def draw(self):
        """Vẽ màn hình."""
        # Xóa màn hình
        self.screen.fill(Colors.BACKGROUND)

        # Vẽ visualization
        self.visualizer.draw()

        # Vẽ UI
        self.btn_generate.draw(self.screen)
        self.btn_start.draw(self.screen)
        self.btn_pause.draw(self.screen)
        self.btn_resume.draw(self.screen)
        self.btn_reset.draw(self.screen)

        # Vẽ sliders với nhãn (bên phải)
        self.slider_size.draw(self.screen)
        size_label = self.label_font.render("Size", True, Colors.TEXT_COLOR)
        self.screen.blit(size_label, (self.slider_size.rect.x, self.slider_size.rect.y - 25))

        self.slider_speed.draw(self.screen)
        speed_label = self.label_font.render("Speed", True, Colors.TEXT_COLOR)
        self.screen.blit(speed_label, (self.slider_speed.rect.x, self.slider_speed.rect.y - 25))

        self.dropdown_algorithm.draw(self.screen)

        # Vẽ thống kê
        self._draw_statistics()

        pygame.display.flip()

    def _draw_statistics(self):
        """Vẽ thống kê."""
        font = pygame.font.Font(None, 20)
        if self.current_algorithm:
            stats = self.current_algorithm.get_statistics().get_stats()
            stats_text = (f"Algorithm: {self.algorithm_name} | "
                         f"Comparisons: {stats['comparisons']} | "
                         f"Swaps: {stats['swaps']} | "
                         f"Time: {stats['execution_time']:.3f}s")
        else:
            stats_text = "Ready to sort..."

        text_surface = font.render(stats_text, True, Colors.TEXT_COLOR)
        self.screen.blit(text_surface, (20, 20))

    def run(self):
        """Chạy ứng dụng."""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()