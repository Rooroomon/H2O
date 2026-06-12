import pygame
import json
import os
from pyvidplayer2 import Video
from pathlib import Path

APP_NAME = "H2O"

save_dir = Path(os.getenv("APPDATA") or Path.home()) / APP_NAME
save_dir.mkdir(parents=True, exist_ok=True)

save_path = save_dir / "save.json"

save_data = None

#세이브 파일 로드
if os.path.exists(save_path):
    with open(save_path, "r", encoding="utf-8") as f:
        save_data = json.load(f)
        stage = save_data["cleared_stage"]
else:
    stage = None

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.3 if save_data == None else save_data["volume"])

from scripts.player_Move import Player
from scripts.ball_Move import Ball
from scripts.tile_manager import TileMap
from scripts.menu import Menu
from scripts.electro import Electro_Object
from scripts.temperature import TemperatureObject
from scripts.slider import Slider

# =========================
# 파일 로드
# =========================
icon = pygame.image.load("./assets/Sprite/Icon.png")
clear_sheet = pygame.image.load("./assets/Sprite/Clear_Sheet.png")
menu_sheet = pygame.image.load("./assets/Sprite/Menu_UI.png")
sun_sprite = pygame.transform.scale(pygame.image.load("./assets/Sprite/Sun.png"), (304, 272))
ground_sprite = pygame.transform.scale(pygame.image.load("./assets/Sprite/Ground.png"), (1024, 256))
player_sheet = pygame.image.load("./assets/Sprite/Player_Sheet.png")

video = Video("./assets/Start_Animation.mp4")
video.set_volume(0.3 if save_data == None else save_data["volume"])

pygame.mixer.music.load("./assets/BGM/MainMenu.mp3")
sound_clear = pygame.mixer.Sound("./assets/SE/Clear.wav")

# =========================
# 스프라이트 설정
# =========================
clearEffect_sprites = []
menu_sprites = []
playerWalk_frames = []
FRAME_W, FRAME_H = 105, 26
clearOffset_x = 377
clearOffset_y = 295

for i in range(32):
    row, col = divmod(i, 1)
    rect = pygame.Rect(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
    clearEffect_sprites.append(pygame.transform.scale(clear_sheet.subsurface(rect), (525, 130)))

menu_sprites.append(pygame.transform.scale(menu_sheet.subsurface((0, 0, 128, 72)), (640, 360)))
menu_sprites.append(pygame.transform.scale(menu_sheet.subsurface((76, 72, 11, 11)), (55, 55)))
menu_sprites.append(pygame.transform.scale(menu_sheet.subsurface((0, 72, 76, 19)), (380, 95)))
menu_sprites.append(pygame.transform.scale(menu_sheet.subsurface((0, 91, 76, 19)), (380, 95)))

playerWalk_frames.append(pygame.transform.scale(player_sheet.subsurface((0, 16, 16, 16)), (128, 128)))
playerWalk_frames.append(pygame.transform.scale(player_sheet.subsurface((16, 16, 16, 16)), (128, 128)))
playerWalk_frames.append(pygame.transform.scale(player_sheet.subsurface((32, 16, 16, 16)), (128, 128)))
playerWalk_frames.append(pygame.transform.scale(player_sheet.subsurface((48, 16, 16, 16)), (128, 128)))
playerWalk_frames.append(pygame.transform.scale(player_sheet.subsurface((64, 16, 16, 16)), (128, 128)))

# =========================
# 설정
# =========================

WIDTH, HEIGHT = 1280, 720
window_width_pre, window_height_pre = 0, 0
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
game_surface = pygame.Surface((WIDTH, HEIGHT))
UI_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
menu_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
scaled_surface = pygame.Surface((WIDTH, HEIGHT))
vid_scale = min(WIDTH / 2560, HEIGHT / 1260)
video.resize((int(2560 * vid_scale), int(1260 * vid_scale)))
pygame.display.set_caption("H2O")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()



font = pygame.font.Font("./assets/NeoDunggeunmo.ttf", 40)
# =========================
# 색상
# =========================
GRAY = (161, 161, 161)
SKY = (128, 233, 255)


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

sound_slider = Slider(WIDTH - 85, HEIGHT - 15, 80, 0, 1, 0.3 if save_data == None else save_data["volume"])
# =========================
# 메인 루프
# =========================
effect = "None"
afterState = "None"
afterMove = False
effectSpeed = 5
alpha = 0
overlay = pygame.Surface(screen.get_size())
overlay.fill((0, 0, 0))
anime_timer = 0
anime_index = 0
event_timer = 0
scroll_x = 0
stage_menu = False
restart_text = font.render("스테이지 재시작", True, (0, 0, 0))
toTitle_text = font.render("타이틀로", True, (0, 0, 0))

state = "title" #"title", "stage"
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
    menu_open = False
    mouseEvent = None
    events = pygame.event.get()
    
    if keys[pygame.K_g]: #치트=====================================
        effect = "clear"
    
    slider_value = sound_slider.handle_event(events)
    pygame.mixer.music.set_volume(slider_value * 0.33 if effect == "clear" else slider_value)
    video.set_volume(slider_value)
    sound_clear.set_volume(slider_value)

    for event in events:
        if event.type == pygame.QUIT:
            #세이브
            new_data = {"volume": sound_slider.value, "cleared_stage": stage}
            
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(new_data, f, indent=4)

            running = False
            video.close()
        elif event.type == pygame.VIDEORESIZE: #화면 크기 변화 ------------------------------------------------
            window_width, window_height = event.size
            UI_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
            menu_overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
            
            scale = min(window_width / WIDTH, window_height / HEIGHT)
            scaled_surface = pygame.Surface((int(WIDTH * scale), int(HEIGHT * scale)))
            menu.change_scale(window_width, window_height)
            overlay = pygame.Surface(screen.get_size())
            overlay.fill((0, 0, 0))
            for i in range(0, len(clearEffect_sprites)):
                clearEffect_sprites[i] = pygame.transform.scale(clearEffect_sprites[i], (525 * scale, 130 * scale))
            clearOffset_x = (window_width - 525 * scale)//2
            clearOffset_y = (window_height - 130 * scale)//2
            vid_scale = min(window_width / 2560, window_height / 1260)
            video.resize((int(2560 * vid_scale), int(1260 * vid_scale)))
            sound_slider.rect.x = window_width - 85
            sound_slider.rect.y = window_height - 15
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                stage_menu = not stage_menu
                canMove = not stage_menu
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            mouseEvent = event
        
        if state == "title" and canMove: #타이틀 버튼들 ------------------------------------------------
            if mouseEvent != None:
                button_interaction = menu.menu_button(event)

    #초기화
    window_width, window_height = pygame.display.get_surface().get_size()

    game_surface.fill(GRAY)
    UI_surface.fill((0, 0, 0, 0))
    screen.fill(GRAY)
        
    # =====================
    # 업데이트
    # =====================
    door_tiles = []
    
    if state == "stage":
        if canMove:
            player.input()

        for obj in objects:
            obj.affect_player(player)
            
        for object in powers:
            object.update(player.state, player, balls, door_tiles, slider_value)
        
        wall_rects = door_tiles + tilemap.wall_rects
        player.physics(slopes, wall_rects)

        player.update_state(slider_value)

        for ball in balls:
            ball.update(slopes, wall_rects, player)
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
        
        
        
        #스테이지 텍스트
        if stage != None:
            stage_text = font.render(f"STAGE {stage + 1}", True, (255, 255, 255))
        
        padding = 5
        text_rect = stage_text.get_rect(topleft = (7, 7))
        bg_rect = pygame.Rect(text_rect.x - padding, text_rect.y - padding, text_rect.width + padding * 2, text_rect.height + padding * 2)
        pygame.draw.rect(UI_surface, (50, 50, 50), bg_rect, 0)
        UI_surface.blit(stage_text, (10, 10))
        
        #메뉴창
        if stage_menu:
            menu_overlay.fill((0, 0, 0, 100))
            restart_rect = pygame.Rect(window_width//2 - 190, window_height//2 - 70, 380, 95)
            toTitle_rect = pygame.Rect(window_width//2 - 190, window_height//2 + 45, 380, 95)
            X_rect = pygame.Rect(window_width//2 + 240, window_height//2 - 160, 55, 55)
            
            UI_surface.blit(menu_overlay, (0, 0))
            UI_surface.blit(menu_sprites[0], (window_width//2 - 320, window_height//2 - 180))
            UI_surface.blit(menu_sprites[1], (window_width//2 + 240, window_height//2 - 160))
            UI_surface.blit(menu_sprites[2], restart_rect.topleft)
            UI_surface.blit(restart_text, restart_text.get_rect(center = restart_rect.center))
            UI_surface.blit(menu_sprites[3], toTitle_rect.topleft)
            UI_surface.blit(toTitle_text, toTitle_text.get_rect(center = toTitle_rect.center))
            
            if mouseEvent != None and mouseEvent.type == pygame.MOUSEBUTTONUP:
                if mouseEvent.button == 1:
                    if restart_rect.collidepoint(mouseEvent.pos):
                        effect = "fade_out"
                        afterState = "stage"
                        afterMove = False
                        effectSpeed = 5
                        
                        stage_menu = False
                    elif toTitle_rect.collidepoint(mouseEvent.pos):
                        effect = "fade_out"
                        afterState = "title"
                        afterMove = False
                        effectSpeed = 5
                        
                        stage_menu = False
                    elif X_rect.collidepoint(mouseEvent.pos):
                        stage_menu = not stage_menu
                        canMove = not stage_menu
            
        
        scale = min(window_width / WIDTH, window_height / HEIGHT)
        scaled_width = int(WIDTH * scale)
        scaled_height = int(HEIGHT * scale)
        
        pygame.transform.scale(game_surface, (scaled_width, scaled_height), scaled_surface)
        screen.blit(scaled_surface, ((window_width - scaled_width)/2, (window_height - scaled_height)/2))
    
        screen.blit(UI_surface, (0, 0))
    elif state == "title": #타이틀 화면 ------------------------------------------------
        menu.draw(screen, window_width, window_height)
        
        if button_interaction == "start":
            pygame.mixer.music.pause()
            
            effect = "fade_out"
            if stage != None:
                afterState = "stage"
            else:
                afterState = "anime"
                stage = 0
                
            afterMove = False
            effectSpeed = 5

        elif button_interaction == "quit":
            #세이브
            new_data = {"volume": sound_slider.value, "cleared_stage": stage}
            
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(new_data, f, indent=4)

            running = False
            video.close()
    elif state == "anime": #초반 애니메이션 ------------------------------------------------
        video.draw(screen, (window_width - 2560 * vid_scale, window_height - 1260 * vid_scale, 1680, 1260))

        video.update() # 비디오 프레임 갱신
        
        #초반 애니메이션 종료
        if not video.active:
            state = "stage"
            pygame.mixer.music.load("./assets/BGM/AdventureofSlime.mp3")
            pygame.mixer.music.play(-1)
            stage = 0
            slopes, powers, objects, balls = tilemap.change_map(stage)
            
            alpha = 255
            effect = "fade_in"
            afterState = "stage"
            stage = 0
            afterMove = True
            effectSpeed = 5
        
        if keys[pygame.K_s]:
            effect = "fade_out"
            afterState = "stage"
            stage = 0
            afterMove = False
            effectSpeed = 5
    elif state == "anime2": #엔딩 화면 ------------------------------------------------
        #연출은 위쪽에
        # 배경------------
        game_surface.fill(SKY)
        
        scroll_x -= 10

        # 이미지 너비만큼 이동하면 원위치
        if scroll_x <= -1024:
            scroll_x = 0

        # 반복해서 그리기
        x = scroll_x
        while x < WIDTH:
            game_surface.blit(ground_sprite, (x, HEIGHT - 256))
            x += 1024
                
        scale = min(window_width / WIDTH, window_height / HEIGHT)
        scaled_width = int(WIDTH * scale)
        scaled_height = int(HEIGHT * scale)
        
        #플레이어-------------
        anime_timer += 1
        if anime_timer >= 5:
            anime_timer = 0
            anime_index = (anime_index + 1) % 5

        img = playerWalk_frames[anime_index]

        game_surface.blit(img, (96, HEIGHT - 256))
        game_surface.blit(sun_sprite, (WIDTH - 304, 0))
        
        pygame.transform.scale(game_surface, (scaled_width, scaled_height), scaled_surface)
        screen.blit(scaled_surface, ((window_width - scaled_width)/2, (window_height - scaled_height)/2))
    
        screen.blit(UI_surface, (0, 0))
        
        #엔딩 종료
        if not pygame.mixer.music.get_busy():
            effect = "fade_out"
            afterState = "title"
            afterMove = False
            effectSpeed = 5
            stage = None
        
        if keys[pygame.K_s]:
            effect = "fade_out"
            afterState = "title"
            afterMove = False
            effectSpeed = 5
            stage = None
            
    
    #최종 출력 ====
    if isClear and canMove:
        anime_timer = 0
        anime_index = 0
        sound_clear.play()
        effect = "clear"
        canMove = False

    if effect == "fade_out": #페이드 아웃 효과 ------------------------------------------------
        if alpha < 255:
            alpha += effectSpeed
            overlay.set_alpha(alpha)
        
            # 현재 화면 위에 덮기
            screen.blit(overlay, (0, 0))
        else:
            overlay.set_alpha(255)
            screen.blit(overlay, (0, 0))
            
            if afterState == "stage" and stage != None and stage >= 0:
                video.close()
                if state != "stage":
                    pygame.mixer.music.load("./assets/BGM/AdventureofSlime.mp3")
                    pygame.mixer.music.play(-1)
                slopes, powers, objects, balls = tilemap.change_map(stage)
            elif afterState == "title":
                pygame.mixer.music.load("./assets/BGM/MainMenu.mp3")
                pygame.mixer.music.play(-1)
            elif afterState == "anime2":
                pygame.mixer.music.load("./assets/BGM/Ending.mp3")
                pygame.mixer.music.play(0)
                
            if afterState != "None":
                state = afterState
            canMove = afterMove
            
            effect = "fade_in"
            afterState = "None"
            afterMove = True
            alpha = 255
            player.rect.x = 150
            player.rect.y = 500
            player.temperature = 0
            player.state = "water"
            camera.x = 150
            camera.y = 500
                
    elif effect == "fade_in": #페이드 인 효과 ------------------------------------------------
        if alpha > 0:
            alpha -= effectSpeed
            overlay.set_alpha(alpha)
    
            # 현재 화면 위에 덮기
            screen.blit(overlay, (0, 0))
        else:
            canMove = afterMove
            
            effect = "None"
            afterState = "None"
            afterMove = False
            alpha = 0
            anime_index = 0
            event_timer = 0
    elif effect == "clear": #스테이지 클리어 효과 ------------------------------------------------
        anime_timer += 1
        event_timer += 1
        
        if anime_timer >= 4:
            anime_timer = 0
            anime_index += 1
        
            if anime_index == 27:
                anime_timer = -60
            elif anime_index == len(clearEffect_sprites):
                anime_index = len(clearEffect_sprites) - 1
                effect = "fade_out"
                if stage <= tilemap.mapCount - 2: #다음 맵 있음
                    afterState = "stage"
                    stage += 1
                else:
                    afterState = "anime2"
                    stage = None
                    anime_index = 0
                afterMove = True
                alpha = 0
        #클리어 연출
        player.vx = 0
        
        if player.state != "water":
            player.change_state()
        
        if event_timer == 80 or event_timer == 150:
            player.vy = -4
            player.rect.y -= 2
            player.animestate = "W_jump"
            
        screen.blit(clearEffect_sprites[anime_index], (clearOffset_x, clearOffset_y))
        
    sound_slider.draw(screen)
    
    #테스트 프레임 ================================================================================
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
    screen.blit(fps_text, (window_width - 175, 20))

    pygame.display.flip()

pygame.quit()