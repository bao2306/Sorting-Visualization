import pygame
from visualization.colors import Colors


class Dropdown:
    """Lớp Dropdown cho giao diện."""

    def __init__(self, x, y, width, height, options):
        """
        Khởi tạo Dropdown.

        Args:
            x, y: Tọa độ
            width, height: Kích thước
            options: Danh sách các tùy chọn
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_index = 0
        self.is_open = False
        self.font = pygame.font.Font(None, 18)
        self.option_height = height

    def get_selected(self):
        """
        Lấy tùy chọn được chọn.

        Returns:
            str: Tùy chọn được chọn
        """
        return self.options[self.selected_index]

    def draw(self, screen):
        # Vẽ button chính
        pygame.draw.rect(screen, Colors.BUTTON_COLOR, self.rect)
        pygame.draw.rect(screen, Colors.WHITE, self.rect, 2)

        # Vẽ text
        text = self.font.render(self.get_selected(), True, Colors.TEXT_COLOR)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

        # Vẽ mũi tên
        arrow_points = [
            (self.rect.right - 15, self.rect.top + 10),
            (self.rect.right - 10, self.rect.top + 10),
            (self.rect.right - 12.5, self.rect.top + 15)
        ]
        pygame.draw.polygon(screen, Colors.TEXT_COLOR, arrow_points)

        # Nếu mở, vẽ các tùy chọn
        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.option_height,
                                          self.rect.width, self.option_height)
                pygame.draw.rect(screen, Colors.BUTTON_HOVER, option_rect)
                pygame.draw.rect(screen, Colors.WHITE, option_rect, 1)

                option_text = self.font.render(option, True, Colors.TEXT_COLOR)
                option_text_rect = option_text.get_rect(center=option_rect.center)
                screen.blit(option_text, option_text_rect)

    def update(self, mouse_pos):
        pass

    def is_clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_open = not self.is_open
            return True

        if self.is_open:
            for i in range(len(self.options)):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.option_height,
                                          self.rect.width, self.option_height)
                if option_rect.collidepoint(mouse_pos):
                    self.selected_index = i
                    self.is_open = False
                    return True

        return False