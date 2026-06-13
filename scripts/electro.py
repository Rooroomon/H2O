import pygame, math, numpy
from scripts.ball_Move import Ball


clock = pygame.time.Clock()
TILE_SIZE = 64
# =========================
# 파일 로드
# =========================
fan_sheet = pygame.image.load("./assets/Sprite/Fan_Sheet.png")
wind_sheet = pygame.image.load("./assets/Sprite/Wind_Sheet.png")
electro_sheet = pygame.image.load("./assets/Sprite/Electronic_Sheet.png")

class Electro_Object:
    def __init__(self, x, y, type, dir = "left"):
        self.x = x
        self.y = y
        self.dir = dir
        self.type = type
        self.offset_x, self.offset_y = 0, 0
        self.anime_timer = 0
        self.anime_index = 0
        self.moving_sprites = []
        self.isOn_pre = False
        
        if type == "fan":
            self.wind_index = 0
            self.wind_sprites = []
            
            self.moving_sprites.append(pygame.transform.scale(fan_sheet.subsurface((0, 0, 16, 24)), (TILE_SIZE * 2, TILE_SIZE * 3)))
            self.moving_sprites.append(pygame.transform.scale(fan_sheet.subsurface((16, 0, 16, 24)), (TILE_SIZE * 2, TILE_SIZE * 3)))
            self.moving_sprites.append(pygame.transform.scale(fan_sheet.subsurface((32, 0, 16, 24)), (TILE_SIZE * 2, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 0, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 24, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 48, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 72, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 96, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 120, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            
            angle = 0
            if dir == "up":
                angle = -90
                self.offset_x, self.offset_y = -1, -1
                self.wind_rect = pygame.Rect(x - TILE_SIZE, y - TILE_SIZE * 6, TILE_SIZE * 3, TILE_SIZE * 5)
            elif dir == "right":
                angle = -180
                self.offset_x, self.offset_y = 0, -1
                self.wind_rect = pygame.Rect(x + TILE_SIZE + 2, y - TILE_SIZE, TILE_SIZE * 5, TILE_SIZE * 3)
            elif dir == "down":
                angle = -270
                self.offset_x, self.offset_y = -1, 0
                self.wind_rect = pygame.Rect(x - TILE_SIZE, y + TILE_SIZE * 2, TILE_SIZE * 3, TILE_SIZE * 5)
            else: #왼쪽
                self.offset_x, self.offset_y = -1, -1
                self.wind_rect = pygame.Rect(x - TILE_SIZE * 6, y - TILE_SIZE, TILE_SIZE * 5, TILE_SIZE * 3)
            
            for i in range(0, len(self.moving_sprites)):
                self.moving_sprites[i] = pygame.transform.rotate(self.moving_sprites[i], angle)
                
            for i in range(0, len(self.wind_sprites)):
                self.wind_sprites[i] = pygame.transform.rotate(self.wind_sprites[i], angle)
        elif type == "door":
            self.Door_off_sprite = pygame.transform.scale(electro_sheet.subsurface((16, 16, 8, 8)), (TILE_SIZE, TILE_SIZE))
            self.Door_on_sprite = pygame.transform.scale(electro_sheet.subsurface((24, 16, 8, 8)), (TILE_SIZE, TILE_SIZE))
            
            self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        elif type == "doorR":
            self.DoorR_off_sprite = pygame.transform.scale(electro_sheet.subsurface((16, 24, 8, 8)), (TILE_SIZE, TILE_SIZE))
            self.DoorR_on_sprite = pygame.transform.scale(electro_sheet.subsurface((24, 24, 8, 8)), (TILE_SIZE, TILE_SIZE))
            
            self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        elif type == "generator":
            self.sprite = pygame.transform.scale(electro_sheet.subsurface((8, 24, 8, 8)), (TILE_SIZE, TILE_SIZE))
                
    def update(self, player, door_rects, isOn, balls):
        if isOn:
            if self.type == "fan":
                if self.wind_rect.colliderect(player.rect):
                    accel = 0.1
                    if player.state != "ice":
                        accel = 0.5
                            
                    if self.dir == "left":
                        player.vx -= accel
                    elif self.dir == "right":
                        player.vx += accel
                    elif self.dir == "up":
                        if not player.on_ground:
                            player.vy -= 0.1
                    elif self.dir == "down":
                        player.vy += 0.1
                
                if len(balls) > 0:
                    for ball in balls:
                        if self.wind_rect.colliderect(ball.rect):
                            accel = 0.15
                                    
                            if self.dir == "left":
                                ball.vx -= accel
                            elif self.dir == "right":
                                ball.vx += accel
                            elif self.dir == "up":
                                ball.vy -= accel
                            elif self.dir == "down":
                                ball.vy += accel
            elif self.type == "door":
                door_rects.append(self.rect)
            elif self.type == "generator" and not self.isOn_pre:
                balls.append(Ball(self.x + TILE_SIZE/2 - 20, self.y + TILE_SIZE/2 - 20, balls, 300))
        else:
            if self.type == "doorR":
                door_rects.append(self.rect)
                
        self.isOn_pre = isOn
        
    
    def draw(self, screen, camera_x, camera_y, WIDTH, HEIGHT, isOn):
        if self.type == "fan":
            if isOn:
                self.anime_timer += 1
                if self.anime_timer >= 5:
                    self.anime_timer = 0
                    self.anime_index = (self.anime_index + 1) % len(self.moving_sprites)
                    self.wind_index = (self.wind_index + 1) % len(self.wind_sprites)
                screen.blit(self.wind_sprites[self.wind_index], (self.wind_rect.x - camera_x + WIDTH / 2, self.wind_rect.y - camera_y + HEIGHT / 2))
                           
            screen.blit(self.moving_sprites[self.anime_index], (self.x - camera_x + WIDTH / 2 + self.offset_x * TILE_SIZE, self.y - camera_y + HEIGHT / 2 + self.offset_y * TILE_SIZE))
        elif self.type == "door":
            img = self.Door_on_sprite if isOn else self.Door_off_sprite
            
            screen.blit(img, (self.x - camera_x + WIDTH / 2, self.y - camera_y + HEIGHT / 2))
        elif self.type == "doorR":
            img = self.DoorR_off_sprite if isOn else self.DoorR_on_sprite
            
            screen.blit(img, (self.x - camera_x + WIDTH / 2, self.y - camera_y + HEIGHT / 2))
        elif self.type == "generator":
            screen.blit(self.sprite, (self.x - camera_x + WIDTH / 2, self.y - camera_y + HEIGHT / 2))
        