import pygame, math, numpy
from pyvidplayer2 import Video

from scripts.player_Move import Player
from scripts.ball_Move import Ball
from scripts.tile_manager import TileMap
from scripts.menu import Menu
from scripts.electro import Electro_Object
from scripts.temperature import TemperatureObject


pygame.init()

# =========================
# 파일 로드
# =========================
icon = pygame.image.load("./assets/Sprite/Icon.png")
video = Video("./assets/Start_Animation.mp4")

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

GROUND = (90, 90, 90)
GRAY = (161, 161, 161)


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

powers = []

objects = []

tilemap = TileMap()
menu = Menu(WIDTH, HEIGHT)
# =========================
# 메인 루프
# =========================
state = "Title" #"Title", "Stage"
canMove = True
running = True

while running:
    dt = clock.tick(FPS)
    button_interaction = "None"

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            #video.close()
        elif event.type == pygame.VIDEORESIZE:
            window_width, window_height = event.size
            UI_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
            
            scale = min(window_width / WIDTH, window_height / HEIGHT)
            scaled_surface = pygame.Surface((int(WIDTH * scale), int(HEIGHT * scale)))
            menu.change_scale(window_width, window_height)
        
        if state == "Title" and canMove:
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_interaction = menu.menu_button(event, "down")
            elif event.type == pygame.MOUSEBUTTONUP:
                button_interaction = menu.menu_button(event, "up")

    #초기화
    window_width, window_height = pygame.display.get_surface().get_size()

    game_surface.fill(GRAY)
    UI_surface.fill((0, 0, 0, 0))
    screen.fill(GRAY)
        
    # =====================
    # 업데이트
    # =====================
    if state == "Stage":
        if canMove:
            player.input()

        for obj in objects:
            obj.affect_player(player)

        player.physics(slopes, tilemap)

        player.update_state()

        for ball in balls:
            ball.update(slopes, tilemap)

        for object in powers:
            object.update(player.rect, player.state, player)
    # =====================
    # 렌더링
    # =====================
        camera.update(window_width, window_height)
    
        tilemap.draw(game_surface, camera.x, camera.y, WIDTH, HEIGHT)


        # 온도 오브젝트
        for obj in objects:
            obj.draw(game_surface, camera.x, camera.y, WIDTH, HEIGHT)

        for slope in slopes:
            slope.draw(game_surface, camera.x, camera.y, WIDTH, HEIGHT)

        for ball in balls:
            ball.draw(game_surface, camera.x, camera.y, WIDTH, HEIGHT)

        for object in powers:
            object.draw(game_surface, camera.x, camera.y, WIDTH, HEIGHT)

        player.draw(game_surface, UI_surface, camera.x, camera.y, WIDTH, HEIGHT)
        
        scale = min(window_width / WIDTH, window_height / HEIGHT)
        scaled_width = int(WIDTH * scale)
        scaled_height = int(HEIGHT * scale)
        
        pygame.transform.scale(game_surface, (scaled_width, scaled_height), scaled_surface)
        screen.blit(scaled_surface, ((window_width - scaled_width)/2, (window_height - scaled_height)/2))
        #screen.blit(scaled_surface, (-(camera.x * scale - window_width // 2), -(camera.y * scale - window_height // 2)))
        #screen.blit(game_surface, (0, 0))
    
        screen.blit(UI_surface, (0, 0))
    else:
        menu.draw(screen, window_width, window_height)
        
        if button_interaction == "start":
            slopes, powers, objects = tilemap.change_map(0) #맵 이동
            state = "Stage"
            canMove = True
        elif button_interaction == "quit":
            running = False
            
    
    #최종 출력 ====  
    
    
    
    
    #테스트 프레임
    fps = clock.get_fps()

    # 글자 Surface 생성
    fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
    
    # 화면 크기에 맞춰 비디오 렌더링 =======================================
    #video.draw(screen, (window_width - 1680, window_height - 1260, 1680, 1260))

    #pygame.display.update()
    #video.update() # 비디오 프레임 갱신
    

    # 화면에 출력
    screen.blit(fps_text, (window_width - 100, 20))

    pygame.display.flip()

pygame.quit()