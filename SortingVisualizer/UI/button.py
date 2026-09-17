import pygame
from visualization.colors import Colors


class Button:
    """Lớp Button cho giao diện."""

    def __init__(self, x, y, width, height, text, color=Colors.BUTTON_COLOR):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = Colors.BUTTON_HOVER
        self.active_color = Colors.BUTTON_ACTIVE
        self.is_hovered = False
        self.is_active = False
        self.font = pygame.font.Font(None, 20)

    def draw(self, screen):

        # Chọn màu
        if self.is_active:
            current_color = self.active_color
        elif self.is_hovered:
            current_color = self.hover_color
        else:
            current_color = self.color

        # Vẽ nút
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, Colors.WHITE, self.rect, 2)

        # Vẽ text
        text_surface = self.font.render(self.text, True, Colors.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def set_active(self, active):
        self.is_active = active