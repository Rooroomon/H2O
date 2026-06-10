import pygame, math, numpy


clock = pygame.time.Clock()
TILE_SIZE = 64
# =========================
# 파일 로드
# =========================
fan_sheet = pygame.image.load("./assets/Sprite/Fan_Sheet.png")
wind_sheet = pygame.image.load("./assets/Sprite/Wind_Sheet.png")

class Electro_Object:
    def __init__(self, x, y, type, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.type = type
        self.offset_x, self.offset_y = 0, 0
        self.anime_timer = 0
        self.anime_index = 0
        self.moving_sprites = []
        
        self.wind_rect = pygame.Rect(x - TILE_SIZE * 6, y - TILE_SIZE, TILE_SIZE * 5, TILE_SIZE * 3)
        
        if type == "fan":
            self.wind_index = 0
            self.wind_sprites = []
            
            self.stop_sprite = pygame.transform.scale(fan_sheet.subsurface((0, 0, 16, 24)), (TILE_SIZE * 2, TILE_SIZE * 3)) #기본 왼쪽
            self.moving_sprites.append(pygame.transform.scale(fan_sheet.subsurface((16, 0, 16, 24)), (TILE_SIZE * 2, TILE_SIZE * 3)))
            self.moving_sprites.append(pygame.transform.scale(fan_sheet.subsurface((32, 0, 16, 24)), (TILE_SIZE * 2, TILE_SIZE * 3)))
            self.moving_sprites.append(pygame.transform.scale(fan_sheet.subsurface((48, 0, 16, 24)), (TILE_SIZE * 2, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 0, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 24, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 48, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 72, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 96, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            self.wind_sprites.append(pygame.transform.scale(wind_sheet.subsurface((0, 120, 40, 24)), (TILE_SIZE * 5, TILE_SIZE * 3)))
            
            angle = 0
            if dir == "up":
                angle = -90
                self.offset_x, self.offset_y = 1, -1
            elif dir == "right":
                angle = -180
                self.offset_x, self.offset_y = 1, 1
            elif dir == "down":
                angle = -270
                self.offset_x, self.offset_y = -1, 1
            else:
                self.offset_x, self.offset_y = -1, -1
                
            self.stop_sprite = pygame.transform.rotate(self.stop_sprite, angle)
            
            for i in range(0, len(self.moving_sprites)):
                self.moving_sprites[i] = pygame.transform.rotate(self.moving_sprites[i], angle)
                
            for i in range(0, len(self.wind_sprites)):
                self.wind_sprites[i] = pygame.transform.rotate(self.wind_sprites[i], angle)
                
    def update(self, player, balls = []):
        if self.type == "fan":
            if self.wind_rect.colliderect(player.rect):
                accel = 0.15
                if player.state == "steam":
                    accel = 0.5
                        
                if self.dir == "left":
                    player.vx -= accel
                elif self.dir == "right":
                    player.vx += accel
                elif self.dir == "up":
                    player.vy -= accel
                elif self.dir == "down":
                    player.vy += accel
            
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
                
        
    
    def draw(self, screen, camera_x, camera_y, WIDTH, HEIGHT, isOn):
        img = self.stop_sprite
        if isOn:
            self.anime_timer += 1
            if self.anime_timer >= 5:
                self.anime_timer = 0
                self.anime_index = (self.anime_index + 1) % len(self.moving_sprites)
                self.wind_index = (self.wind_index + 1) % len(self.wind_sprites)
            screen.blit(self.wind_sprites[self.wind_index], (self.x - camera_x + WIDTH / 2 + self.offset_x * TILE_SIZE * 6, self.y - camera_y + HEIGHT / 2 + self.offset_y * TILE_SIZE))
                       
        screen.blit(self.moving_sprites[self.anime_index], (self.x - camera_x + WIDTH / 2 + self.offset_x * TILE_SIZE, self.y - camera_y + HEIGHT / 2 + self.offset_y * TILE_SIZE))            
        