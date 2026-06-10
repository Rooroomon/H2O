import pygame, math, numpy

# =========================
# 파일 로드
# =========================


# =========================
# 온도 오브젝트
# =========================

class TemperatureObject:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind  # "hot" or "cold"
        
        sheet = pygame.image.load("./assets/Sprite/TempObject_Sheet.png").convert_alpha()
        
        if kind == "cold":
            self.sprite = pygame.transform.scale(sheet.subsurface((0, 0, 24, 24)), (120, 120))
        else:
            self.sprite = pygame.transform.scale(sheet.subsurface((24, 0, 24, 24)), (120, 120))

    def draw(self, screen, camera_x, camera_y, WIDTH, HEIGHT):
        screen.blit(self.sprite, (self.x - camera_x + WIDTH / 2 - 20, self.y - camera_y + HEIGHT / 2 - 20))

    def affect_player(self, player):
        dx = self.x - player.rect.x
        dy = self.y - player.rect.y
        dist = math.hypot(dx, dy)

        if dist < 110:
            if self.kind == "hot":
                player.temperature += 0.75
            else:
                player.temperature -= 0.75
            player.temp_clock = 0