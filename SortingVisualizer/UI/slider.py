import pygame
from visualization.colors import Colors


class Slider:
    """Lớp Slider cho giao diện."""

    def __init__(self, x, y, width, height, min_val=1, max_val=100, initial=50):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = initial
        self.is_dragging = False
        self.knob_radius = 10
        self.font = pygame.font.Font(None, 16)

    def get_knob_x(self):
        ratio = (self.current_val - self.min_val) / (self.max_val - self.min_val)
        return self.rect.x + ratio * self.rect.width

    def draw(self, screen):
        # Vẽ thanh trượt
        pygame.draw.rect(screen, Colors.GRAY, self.rect)
        pygame.draw.rect(screen, Colors.WHITE, self.rect, 2)

        # Vẽ knob
        knob_x = self.get_knob_x()
        pygame.draw.circle(screen, Colors.BUTTON_COLOR, (int(knob_x), self.rect.centery), self.knob_radius)

        # Vẽ giá trị - đặt bên PHẢI thanh trượt để luôn nhìn thấy rõ, không bị
        # đè lên nhãn (label) vẽ phía trên thanh trượt.
        value_text = self.font.render(f"{self.current_val}", True, Colors.TEXT_COLOR)
        value_rect = value_text.get_rect(midleft=(self.rect.right + 12, self.rect.centery))
        screen.blit(value_text, value_rect)

    def start_drag(self, mouse_pos):
        """
        Bắt đầu kéo thanh trượt - CHỈ khi người dùng thực sự bấm chuột
        (MOUSEBUTTONDOWN) trúng vào knob hoặc thanh trượt.
        Gọi hàm này từ sự kiện MOUSEBUTTONDOWN, không gọi khi chuột chỉ di chuyển ngang qua.

        Args:
            mouse_pos: Tọa độ chuột lúc nhấn
        """
        knob_x = self.get_knob_x()
        knob_rect = pygame.Rect(knob_x - self.knob_radius, self.rect.centery - self.knob_radius,
                                self.knob_radius * 2, self.knob_radius * 2)

        if knob_rect.collidepoint(mouse_pos) or self.rect.collidepoint(mouse_pos):
            self.is_dragging = True
            self._set_value_from_pos(mouse_pos)

    def update(self, mouse_pos):
        """
        Cập nhật slider khi chuột di chuyển.
        CHỈ cập nhật giá trị nếu đang trong trạng thái kéo (is_dragging=True),
        tức là người dùng đã bấm chuột trước đó (xem start_drag). Việc chỉ
        rê chuột ngang qua thanh trượt sẽ KHÔNG làm thay đổi giá trị nữa.

        Args:
            mouse_pos: Tọa độ chuột
        """
        if self.is_dragging:
            self._set_value_from_pos(mouse_pos)

    def _set_value_from_pos(self, mouse_pos):
        """Tính giá trị mới của slider dựa theo vị trí X của chuột."""
        x = max(self.rect.x, min(mouse_pos[0], self.rect.x + self.rect.width))
        ratio = (x - self.rect.x) / self.rect.width
        self.current_val = int(self.min_val + ratio * (self.max_val - self.min_val))
        self.current_val = max(self.min_val, min(self.max_val, self.current_val))

    def on_mouse_release(self):
        """Khi thả chuột."""
        self.is_dragging = False

    def get_value(self):
        """
        Lấy giá trị hiện tại.

        Returns:
            int: Giá trị slider
        """
        return self.current_val