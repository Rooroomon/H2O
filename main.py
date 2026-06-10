import pygame, math, numpy
#from pyvidplayer2 import Video

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.3)

from scripts.player_Move import Player
from scripts.ball_Move import Ball
from scripts.tile_manager import TileMap
from scripts.menu import Menu
from scripts.electro import Electro_Object
from scripts.temperature import TemperatureObject


# =========================
# 파일 로드
# =========================
icon = pygame.image.load("./assets/Sprite/Icon.png")
clear_sheet = pygame.image.load("./assets/Sprite/Clear_Sheet.png")
#video = Video("./assets/Start_Animation.mp4")
pygame.mixer.music.load("./assets/BGM/MainMenu.mp3")
#BGM_menu = pygame.mixer.Sound("./assets/BGM/MainMenu.mp3")

# =========================
# 스프라이트 설정
# =========================
clearEffect_frames = []
FRAME_W, FRAME_H = 105, 26
clearOffset_x = 377
clearOffset_y = 295

for i in range(32):
    row, col = divmod(i, 1)
    rect = pygame.Rect(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
    clearEffect_frames.append(pygame.transform.scale(clear_sheet.subsurface(rect), (525, 130)))

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
GRAY = (161, 161, 161)


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

balls = []

powers = []

objects = []

player = Player()
tilemap = TileMap()

menu = Menu(WIDTH, HEIGHT)
# =========================
# 메인 루프
# =========================
effect = "None"
afterState = "None"
afterStage = -1
afterMove = False
effectSpeed = 5
alpha = 0
overlay = pygame.Surface(screen.get_size())
overlay.fill((0, 0, 0))
anime_timer = 0
anime_index = 0
event_timer = 0

state = "title" #"title", "stage"
stage = -1
canMove = True
running = True

# 2. 배경음악 재생 (-1: 무한 반복)
pygame.mixer.music.play(-1)

# 3. 추가 제어 함수
#pygame.mixer.music.stop()   # 음악 정지
#pygame.mixer.music.pause()  # 음악 일시정지
#pygame.mixer.music.unpause() # 음악 일시정지 해제

while running:
    dt = clock.tick(FPS)
    button_interaction = "None"
    keys = pygame.key.get_pressed()
    isClear = False
    if keys[pygame.K_g]:
        effect = "clear"

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
            overlay = pygame.Surface(screen.get_size())
            overlay.fill((0, 0, 0))
            for i in range(0, len(clearEffect_frames)):
                clearEffect_frames[i] = pygame.transform.scale(clearEffect_frames[i], (525 * scale, 130 * scale))
            clearOffset_x = (window_width - 525 * scale)//2
            clearOffset_y = (window_height - 130 * scale)//2
        
        if state == "title" and canMove:
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
    if state == "stage":
        if canMove:
            player.input()

        for obj in objects:
            obj.affect_player(player)

        player.physics(slopes, tilemap)

        player.update_state()

        for ball in balls:
            ball.update(slopes, tilemap, player)

        for object in powers:
            object.update(player.state, player, balls)
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
        isClear = player.is_clear(tilemap)
        
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
            effect = "fade_out"
            afterState = "stage"
            afterStage = 0
            afterMove = False
            effecteffectSpeed = 3
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
    if isClear and canMove:
        effect = "clear"
        canMove = False
        anime_timer = 0
        anime_index = 0

    if effect == "fade_out":
        if alpha < 255:
            alpha += effectSpeed
            overlay.set_alpha(alpha)
        
            # 현재 화면 위에 덮기
            screen.blit(overlay, (0, 0))
        else:
            overlay.set_alpha(255)
            screen.blit(overlay, (0, 0))
            
            if afterState != "None":
                state = afterState
            canMove = afterMove
            if state == "stage" and afterStage != stage and afterStage >= 0:
                stage = afterStage
                slopes, powers, objects, balls = tilemap.change_map(stage)
            
            effect = "fade_in"
            afterState = "None"
            afterStage = -1
            afterMove = True
            alpha = 255
            player.rect.x = 150
            player.rect.y = 500
            camera.x = 150
            camera.y = 500
                
    elif effect == "fade_in":
        if alpha > 0:
            alpha -= effectSpeed
            overlay.set_alpha(alpha)
    
            # 현재 화면 위에 덮기
            screen.blit(overlay, (0, 0))
        else:
            if afterState != "None":
                state = afterState
            canMove = afterMove
            if state == "stage" and afterStage != stage and afterStage >= 0:
                stage = afterStage
                slopes, powers, objects = tilemap.change_map(stage)
            
            effect = "None"
            afterState = "None"
            afterStage = -1
            afterMove = False
            alpha = 0
    elif effect == "clear":
        anime_timer += 1
        event_timer += 1
        
        if anime_timer >= 4:
            anime_timer = 0
            anime_index += 1
        
            if anime_index == 27:
                anime_timer = -60
            elif anime_index == len(clearEffect_frames):
                anime_index = len(clearEffect_frames) - 1
                effect = "fade_out"
                if stage <= tilemap.mapCount - 2: #다음 맵 있음
                    afterState = "stage"
                    afterStage = stage + 1
                else:
                    afterState = "title"
                    afterStage = -1
                afterMove = True
                alpha = 0
            
        #연출
        player.vx = 0
        
        if player.state != "water":
            player.change_state()
        
        if event_timer == 80 or event_timer == 150:
            player.vy = -4
            player.rect.y -= 2
            player.animestate = "W_jump"
            
        screen.blit(clearEffect_frames[anime_index], (clearOffset_x, clearOffset_y))
    

    # 화면에 출력
    screen.blit(fps_text, (window_width - 100, 20))

    pygame.display.flip()

pygame.quit()