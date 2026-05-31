import pygame, math, numpy
from pyvidplayer2 import Video

from scripts.player_Move import Player
from scripts.ball_Move import Ball
from scripts.tile_manager import TileMap


pygame.init()

# =========================
# 파일 로드
# =========================
icon = pygame.image.load("./assets/Sprite/Icon.png")
#video = Video("./assets/Start_Animation.mp4")

# =========================
# 설정
# =========================

WIDTH, HEIGHT = 1280, 720
window_width_pre, window_height_pre = 0, 0
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
game_surface = pygame.Surface((1280, 720))
UI_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
scaled_surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("H2O")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()



font = pygame.font.SysFont(None, 30)
# =========================
# 색상
# =========================

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)

RED = (255, 100, 100)
CYAN = (100, 255, 255)

GROUND = (90, 90, 90)
GRAY = (161, 161, 161)

# =========================
# 온도 오브젝트
# =========================

class TemperatureObject:
    def __init__(self, x, y, radius, kind):
        self.x = x
        self.y = y
        self.radius = radius
        self.kind = kind  # "hot" or "cold"

    def draw(self, screen, camera_x, camera_y):
        color = RED if self.kind == "hot" else CYAN
        pygame.draw.circle(screen, color, (self.x - camera_x + WIDTH / 2, self.y - camera_y + HEIGHT / 2), self.radius)

    def affect_player(self, player):
        dx = self.x - player.rect.x
        dy = self.y - player.rect.y
        dist = math.hypot(dx, dy)

        if dist < self.radius + 80:
            if self.kind == "hot":
                player.temperature += 0.5
            else:
                player.temperature -= 0.5
            player.temp_clock = 0


objects = [
    TemperatureObject(450, 430, 30, "hot"),
    TemperatureObject(850, 330, 30, "cold"),
]



# =========================
# 플레이어
# =========================



player = Player()

# ==================================================
# 카메라
# ==================================================
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        512, 288
        

    def update(self, width, height):
        self.x += (player.rect.x + player.width / 2 - self.x) * 0.05
        self.y += (player.rect.y - 50 - self.y) * 0.05
        
camera = Camera()

# ==================================================
# 맵
# ==================================================
slopes = []

balls = [
    Ball(300, 100, 20)
]

tilemap = TileMap()
# =========================
# 메인 루프
# =========================
a = 0
running = True

while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            #video.close()
        elif event.type == pygame.VIDEORESIZE:
            window_width, window_height = event.size
            UI_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
            
            scale = min(window_width / WIDTH, window_height / HEIGHT)
            scaled_surface = pygame.Surface((int(WIDTH * scale), int(HEIGHT * scale)))
        
    # =====================
    # 업데이트
    # =====================
    a += dt
    if a // 1000 == 5:
        a = 10000000
        slopes = tilemap.change_map(0)
        
    player.input()

    for obj in objects:
        obj.affect_player(player)

    player.physics(slopes, tilemap)

    player.update_state()
    
    for ball in balls:
        ball.update(slopes, tilemap)

    # =====================
    # 렌더링
    # =====================
    
    #초기화
    window_width, window_height = pygame.display.get_surface().get_size()
    
    camera.update(window_width, window_height)
    
    game_surface.fill(GRAY)
    UI_surface.fill((0, 0, 0, 0))

    
    tilemap.draw(game_surface, camera.x, camera.y, WIDTH, HEIGHT)
    

    # 오브젝트
    for obj in objects:
        obj.draw(game_surface, camera.x, camera.y)
        

    # 플레이어
    player.draw(game_surface, UI_surface, camera.x, camera.y, WIDTH, HEIGHT)
    
    for slope in slopes:
        slope.draw(game_surface, camera.x, camera.y, WIDTH, HEIGHT)

    for ball in balls:
        ball.draw(game_surface, camera.x, camera.y, WIDTH, HEIGHT)
    
    
    #최종 출력 ====  
    screen.fill(GRAY)
    
    scale = min(window_width / WIDTH, window_height / HEIGHT)
    scaled_width = int(WIDTH * scale)
    scaled_height = int(HEIGHT * scale)
    
    pygame.transform.scale(game_surface, (scaled_width, scaled_height), scaled_surface)
    screen.blit(scaled_surface, ((window_width - scaled_width)/2, (window_height - scaled_height)/2))
    #screen.blit(scaled_surface, (-(camera.x * scale - window_width // 2), -(camera.y * scale - window_height // 2)))
    #screen.blit(game_surface, (0, 0))
    
    screen.blit(UI_surface, (0, 0))
    
    #테스트 프레임
    fps = clock.get_fps()

    # 글자 Surface 생성
    fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
    #fps_text = font.render(f"Window_Scale: {window_width} {window_height}", True, (255, 255, 255))'
    
    # 화면 크기에 맞춰 비디오 렌더링 =======================================
    #video.draw(screen, (window_width - 1680, window_height - 1260, 1680, 1260))

    #pygame.display.update()
    #video.update() # 비디오 프레임 갱신
    

    # 화면에 출력
    screen.blit(fps_text, (window_width - 100, 20))

    pygame.display.flip()

pygame.quit()