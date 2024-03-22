import pygame

class Button:
    def __init__(self, x, y, width, height, text=None, color=(73, 73, 73), text_color=(255, 255, 255), font_size=30):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font_size = font_size

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.text:
            font = pygame.font.Font(None, self.font_size)
            text_surf = font.render(self.text, True, self.text_color)
            screen.blit(text_surf, (self.x + (self.width - text_surf.get_width()) / 2,
                                    self.y + (self.height - text_surf.get_height()) / 2))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False
