import pygame, math, numpy

# =========================
# 경사
# =========================
class Slope:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

    def draw(self, screen, camera_x, camera_y, WIDTH, HEIGHT):
        pygame.draw.line(
            screen,
            (180, 180, 180),
            (self.x1 - camera_x + WIDTH / 2, self.y1 - camera_y + HEIGHT / 2 + 2),
            (self.x2 - camera_x + WIDTH / 2, self.y2 - camera_y + HEIGHT / 2 + 2),
            6
        )

    def get_y(self, x):

        # x 위치에 따른 경사 y 계산
        t = (x - self.x1) / (self.x2 - self.x1)

        return self.y1 + (self.y2 - self.y1) * t