import pygame
from scripts.electro import Electro_Object

# =========================
# 파일 로드
# =========================
sheet = pygame.image.load("./assets/Sprite/Electronic_Sheet.png")

sound_on = pygame.mixer.Sound("./assets/SE/Plate_On.wav")
sound_off = pygame.mixer.Sound("./assets/SE/Plate_Off.wav")

# =========================
# 스프라이트 설정
# =========================
sprites = []
TILE_SIZE = 64

sprites.append(pygame.transform.scale(sheet.subsurface((0, 0, 8, 8)), (TILE_SIZE, TILE_SIZE))) #배터리
sprites.append(pygame.transform.scale(sheet.subsurface((0, 8, 8, 8)), (TILE_SIZE, TILE_SIZE))) #빛 감지기
sprites.append(pygame.transform.scale(sheet.subsurface((0, 16, 8, 8)), (TILE_SIZE, TILE_SIZE))) #발판 OFF
sprites.append(pygame.transform.scale(sheet.subsurface((8, 16, 8, 8)), (TILE_SIZE, TILE_SIZE))) #발판 ON

class PowerSource:
    def __init__(self, x, y, type): #타입 종류: battery, detector, plate
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.type = type
        self.target = None
        self.isOn = False
        self.isOn_pre = False
        
    def update(self, player_state, player, balls, door_rects, volume):
        self.isOn = False
        
        if self.type == "battery":
            self.isOn = True
        elif self.type == "detector":
            self.isOn = True #이거 조건 정해야 됨
        elif self.type == "plate":
            sound_on.set_volume(volume)
            sound_off.set_volume(volume)
            
            for ball in balls:
                if self.rect.colliderect(ball.rect):
                    self.isOn = True
                    break
                
            if self.rect.colliderect(player.rect) and player_state != "steam":
                self.isOn = True
              
            if self.isOn and not self.isOn_pre: #이번에 켜짐
                sound_on.play()
            elif not self.isOn and self.isOn_pre: #이번에 꺼짐
                sound_off.play()

            self.isOn_pre = self.isOn
                
        if self.isOn and self.target != None:
            self.target.update(player, door_rects, balls)
            
        
    def draw(self, screen, camera_x, camera_y, WIDTH, HEIGHT):
        sprite_index = 0
        
        if self.type == "battery":
            sprite_index = 0
        elif self.type == "detector" and self.isOn:
            sprite_index = 1
        elif self.type == "plate":
            if self.isOn:
                sprite_index = 3
            else:
                sprite_index = 2
            
            
        screen.blit(sprites[sprite_index], (self.rect.x - camera_x + WIDTH / 2, self.rect.y - camera_y + HEIGHT / 2))
        
        if self.target != None:
            self.target.draw(screen, camera_x, camera_y, WIDTH, HEIGHT, self.isOn)