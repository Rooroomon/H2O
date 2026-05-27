import pygame, math, numpy
from player_Move import Player
from pyvidplayer2 import Video
from tile_manager import TileMap


pygame.init()

# =========================
# 파일 로드
# =========================
icon = pygame.image.load("./assets/Sprite/Icon.png")
#video = Video("./assets/Start_Animation.mp4")

# =========================
# 설정
# =========================

WIDTH, HEIGHT = 1080, 720
window_width_pre, window_height_pre = 0, 0
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
game_surface = pygame.Surface((6400, 3200))
UI_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
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

    def draw(self, screen):
        color = RED if self.kind == "hot" else CYAN
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

    def affect_player(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
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
# 경사
# =========================
class Slope:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

    def draw(self, screen):
        pygame.draw.line(
            screen,
            (180, 180, 180),
            (self.x1, self.y1 + 4),
            (self.x2, self.y2 + 4),
            6
        )

    def get_y(self, x):

        # x 위치에 따른 경사 y 계산
        t = (x - self.x1) / (self.x2 - self.x1)

        return self.y1 + (self.y2 - self.y1) * t


# =========================
# 공
# =========================
class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y

        self.radius = radius

        self.vx = 0
        self.vy = 0

    def update(self):

        # 중력
        self.vy += 0.4

        self.x += self.vx
        self.y += self.vy
        
        # 경사 충돌    
        for slope in slopes:

            if slope.x1 <= self.x <= slope.x2:

                slope_y = slope.get_y(self.x)

                feet = self.y + self.radius

                if feet >= slope_y and feet <= slope_y + 15:

                    self.y = slope_y - self.radius

                    self.vy = 0

                    # 경사 방향 계산
                    dx = slope.x2 - slope.x1
                    dy = slope.y2 - slope.y1

                    angle = math.atan2(dy, dx)

                    # 경사 따라 굴러감
                    self.vx += math.cos(angle) * 0.5 * numpy.sign(angle)
                    
                    
        tile_x1, tile_y = tilemap.world_to_tile(self.x, self.y)
        tile_x2 = tilemap.world_to_tile(self.x + 50, self.y)[0]
        tile_x1 = (int)(tile_x1)
        tile_x2 = (int)(tile_x2)
        tile_y = (int)(tile_y)
        tileType1 = tilemap.test_solid(tile_x1, tile_y)
        tileType2 = tilemap.test_solid(tile_x2, tile_y)
                    
        #벽
        if tileType1 == "Wall" or tileType1 == "Ground":
            if self.y <= tilemap.tile_to_world(tile_x1, tile_y)[1] + self.radius * 2 - 5:
                self.x = max(tilemap.tile_to_world(tile_x1, tile_y)[0] + 56, self.x)
        
        if tileType2 == "Wall" or tileType2 == "Ground":
            if self.y <= tilemap.tile_to_world(tile_x1, tile_y)[1] + self.radius * 2 - 5:
                self.x = min(tilemap.tile_to_world(tile_x2, tile_y)[0] - self.radius * 2, self.x)
        
        #바닥
        if tilemap.test_solid(tile_x1, tile_y) == "Ground" or tilemap.test_solid(tile_x2, tile_y) == "Ground":
            if self.vy >= 0:
                self.y = tilemap.tile_to_world(tile_x1, tile_y)[1] - self.radius - 1
                self.vy = 0
                
        print(f"{self.y}")

        # 마찰
        self.vx *= 0.99

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            (255, 200, 100),
            (int(self.x), int(self.y)),
            self.radius
        )
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
        #if player.x < self.x + WIDTH / 2 - 256 or player.x > self.x + WIDTH / 2 + 256:
        #    self.x += (-(player.x - WIDTH / 2) - self.x) * 0.1
            
        #if player.y < self.y + HEIGHT / 2 - 144 or player.y > self.y + HEIGHT / 2 + 144:
        #    self.y += (-(player.y - HEIGHT / 2) - self.y) * 0.1
        
        self.x += (-(player.x - width / 2) - self.x) * 0.05
        self.y += (-(player.y - height / 2) - self.y) * 0.05
        
camera = Camera()

# ==================================================
# 맵
# ==================================================
slopes = [
    Slope(200, 600, 500, 450),
    Slope(700, 500, 1000, 600),
]

balls = [
    Ball(300, 100, 20)
]

tilemap = TileMap()
# =========================
# 메인 루프
# =========================

running = True

while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            #video.close()

    # =====================
    # 업데이트
    # =====================

    player.input()

    for obj in objects:
        obj.affect_player(player)

    player.physics(slopes, tilemap)

    player.update_state()
    
    for ball in balls:
        ball.update()

    # =====================
    # 렌더링
    # =====================
    
    #초기화
    window_width, window_height = pygame.display.get_surface().get_size()
    
    game_surface.fill(GRAY)
    
    if window_width_pre != window_width or window_height_pre != window_height:
        UI_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    else:
        UI_surface.fill((0, 0, 0, 0))
    
    window_width_pre = window_width
    window_height_pre = window_height
    
    #카메라 이동
    camera.update(window_width, window_height)

    # 오브젝트
    for obj in objects:
        obj.draw(game_surface)
        
    tilemap.draw(game_surface)

    # 플레이어
    player.draw(game_surface, UI_surface)
    
    for slope in slopes:
        slope.draw(game_surface)

    for ball in balls:
        ball.draw(game_surface)
    
    
    #최종 출력 ====    
    screen.fill(GRAY)
    
    screen.blit(game_surface, (camera.x, camera.y))
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