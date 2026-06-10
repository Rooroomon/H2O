import pygame, math, numpy

# =========================
# 색상
# =========================
WHITE = (255, 255, 255)


# =========================
# 파일 로드
# =========================
player_sheet = pygame.image.load("./assets/Sprite/Player_Sheet.png")
gauge_sheet = pygame.image.load("./assets/Sprite/Gauge.png")


# =========================
# 스프라이트 설정
# =========================
player_frames = []
gauge_sprites = []
FRAME_W, FRAME_H = 16, 16
COLS = 11

for i in range(165):
    row, col = divmod(i, COLS)
    rect = pygame.Rect(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
    player_frames.append(pygame.transform.scale(player_sheet.subsurface(rect), (56, 56)))
    
playerW_idle = [player_frames[i] for i in [0, 1]]
playerW_walk = [player_frames[i] for i in [11, 12, 13, 14, 15]]
playerW_jump = [player_frames[i] for i in [23, 24 ,25, 26]]
playerW_fall = [player_frames[i] for i in [33, 34, 35, 36]]
playerW_falling = [player_frames[i] for i in [36]]
playerW_land = [player_frames[i] for i in [44, 45, 46, 47]]
playerW_freeze = [player_frames[i] for i in [55, 56, 57, 58, 59, 66, 67, 68, 69]]
playerW_evaporate = [player_frames[i] for i in [110, 111, 112, 113, 121, 122 ,123, 124]]

playerI_idle = [player_frames[i] for i in [77]]
playerI_unfreeze = [player_frames[i] for i in [88, 89, 90, 91, 92, 99, 100, 101, 102]]

playerC_idle = [player_frames[i] for i in [132]]
playerC_condensation = [player_frames[i] for i in [143, 144, 145, 146, 154, 155, 156, 157]]

gauge_sprites.append(pygame.transform.scale(gauge_sheet.subsurface((0, 0, 25, 77)), (75, 231)))
gauge_sprites.append(pygame.transform.scale(gauge_sheet.subsurface((25, 0, 25, 77)), (75, 231)))
gauge_sprites.append(pygame.transform.scale(gauge_sheet.subsurface((50, 0, 25, 77)), (75, 231)))
gauge_sprites.append(pygame.transform.scale(gauge_sheet.subsurface((75, 0, 25, 77)), (75, 231)))
gauge_sprites.append(pygame.transform.scale(gauge_sheet.subsurface((100, 0, 25, 77)), (75, 231)))

clock = pygame.time.Clock()


TILE_SIZE = 56

def check_collision(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def is_collide(rect, tiles):
    for tile in tiles:
        if rect.colliderect(tile):
            return True

    return False

class Player:
    def __init__(self):
        self.vx = 0
        self.vy = 0

        self.width = 56
        self.height = 56
        
        self.rect = pygame.Rect(150, 500, self.width, self.height)
        
        self.dir = 1
        self.land = "ground"

        self.on_ground = False
        self.landslope = None
        
        self.movedelay = 0
        
        self.transCool = 0

        # 상태
        self.state = "water"
        self.animestate = "W_idle"
        self.animestate_pre = "W_idle"

        # 온도
        self.temperature = 0
        self.temp_clock = 0

        # 상태 타이머
        self.anime_end = False
        
        self.state_timer = 0
        self.anime_timer = 0
        self.anime_index = 0
        self.anime_speed = 0

    # =========================
    # 클리어 처리
    # =========================
    
    def is_clear(self, tilemap):
        for tile_rect in tilemap.clear_rects:
            if self.rect.colliderect(tile_rect):
                return True
        return False

    # =========================
    # 입력 처리
    # =========================

    def input(self):
        keys = pygame.key.get_pressed()
        
        if self.transCool < 0 and keys[pygame.K_f]:
            self.change_state()
        else:
            self.transCool -= 1
        
        #치트
        if keys[pygame.K_q]:
            self.temperature = -150
        elif keys[pygame.K_e]:
            self.temperature = 150
        
        if(self.movedelay > 0):
            self.movedelay -= 1
        else:
            # ---------------------
            # 물
            # ---------------------
            if self.state == "water":
                accel = 0.75
                max_speed = 4
    
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.vx -= accel
                    if self.on_ground:
                        self.animestate = "W_walk"
                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.vx += accel
                    if self.on_ground:
                        self.animestate = "W_walk"
                else:
                    self.vx *= 0.75
                    
                self.vx = max(-max_speed, min(max_speed, self.vx))
    
                # 점프
                if keys[pygame.K_SPACE] and self.on_ground:
                    self.vy = -7
                    self.rect.y -= 2
                    self.animestate = "W_jump"
                    
                if not self.on_ground and self.state == "water":
                    if self.animestate != "W_jump" and self.animestate != "W_fall" and self.animestate != "W_falling":
                        self.animestate = "W_fall"
    
            # ---------------------
            # 얼음
            # ---------------------
            elif self.state == "ice":
                accel = 0.2
                max_speed = 6
    
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.vx -= accel
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.vx += accel
    
                # 마찰 적음
                self.vx *= 0.98
    
                self.vx = max(-max_speed, min(max_speed, self.vx))
    
            # ---------------------
            # 수증기
            # ---------------------
            elif self.state == "steam":
                accel = 0.35
                max_speed = 4
    
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.vx -= accel
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.vx += accel
    
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    self.vy -= accel
    
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    self.vy += accel
    
                self.vx *= 0.95
                self.vy *= 0.95
    
                self.vx = max(-max_speed, min(max_speed, self.vx))
                self.vy = max(-max_speed, min(max_speed, self.vy))
    
    def change_state(self):
        if self.state == "water":
            if self.temperature >= 100:
                self.state = "steam"
                self.movedelay = 36
                self.animestate = "W_eva"
                self.transCool = 60
            elif self.temperature <= -100:
                self.state = "ice"
                self.movedelay = 40
                self.animestate = "W_freeze"
                self.transCool = 60
        else:
            if self.state == "steam":
                self.animestate = "C_con"
                self.movedelay = 36
                self.transCool = 60
            elif self.state == "ice":
                self.animestate = "I_unfreeze"
                self.movedelay = 40
                self.transCool = 60
                
            self.state = "water"

    # =========================
    # 물리
    # =========================

    def physics(self, slopes, tilemap):
        dt = clock.tick(60) / 1000
        self.temp_clock += dt
        
        
        if self.state != "water":
            self.temperature -= numpy.sign(self.temperature) * dt * 20
        elif self.temp_clock > 4:
            self.temperature -= numpy.sign(self.temperature) * dt * 7.5
            if abs(self.temperature) < 1:
                self.temp_clock = -500
                
        self.temperature = max(-150, min(self.temperature, 150))
                

        # 중력
        if self.state != "steam" and not self.on_ground:
            if abs(self.vy) < 0:
                self.vy += 0.35
            else:
                self.vy += 0.25
                
        self.vy = min(15, self.vy)

        self.on_ground = False

        prev_rect = self.rect.copy()
        
        if abs(self.vx) < 0.05:
            self.vx = 0
        if abs(self.vy) < 0.05:
            self.vy = 0
        
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        #지형 충돌
        collide_list = check_collision(self.rect, tilemap.wall_rects)
        side = set()

        for rect in collide_list:
            overlap = self.rect.clip(rect)

            if overlap.width > 0 and overlap.height > 0:
                if overlap.width < overlap.height:
                    # 좌우 충돌
                    if self.rect.centerx < rect.centerx:
                        side.add("right")   # rect1의 오른쪽 면이 rect2에 닿음
                    else:
                        side.add("left")
                else:
                    # 상하 충돌
                    if self.rect.centery < rect.centery:
                        side.add("bottom")  # rect1의 아래쪽 면이 rect2에 닿음
                    else:
                        side.add("top")

        
        # 1. X축 이동 및 충돌 처리
        self.rect.topleft = (self.rect.x, self.rect.y)
        Xhit_list = check_collision(self.rect, tilemap.wall_rects)
        for tile in Xhit_list:
            if self.vx >= 0 and self.rect.x < tile.left - 40 and "right" in side:
                self.vx = 0
                self.rect.right = tile.left
            elif self.vx <= 0 and self.rect.x > tile.right - 16 and "left" in side:
                self.vx = 0
                self.rect.left = tile.right
    
        # 2. 바닥
        self.rect.topleft = (self.rect.x, self.rect.y)
        Yhit_list = check_collision(self.rect, tilemap.wall_rects)
        for tile in Yhit_list:
            if self.vy >= 0 and self.rect.y < tile.top - 40 and "bottom" in side:
                self.vy = 0
                self.rect.bottom = tile.top + 1
                self.on_ground = True
                if self.animestate == "W_fall" or self.animestate == "W_falling":
                        self.animestate = "W_land"
                
        # 3. 천장
        for tile in Yhit_list:
            if self.vy <= 0 and self.rect.y > tile.bottom - 6 and "top" in side:
                self.vy = 0
                self.rect.top = tile.bottom
            
            
        #경사 충돌
        self.land = "none"
            
        for slope in slopes:

            if slope.x1 <= self.rect.x + self.width/2 <= slope.x2:

                slope_y = slope.get_y(self.rect.x + self.width/2)

                feet = self.rect.y + self.height

                # 경사 위에 착지
                if feet >= slope_y - 5 and feet <= slope_y + 25 and self.vy >= 0:
                    self.land = "slope"
                    self.landslope = slope

                    self.rect.y = slope_y - self.height
                    self.vy = 0
                    self.on_ground = True
                    if self.animestate == "W_fall" or self.animestate == "W_falling":
                        self.animestate = "W_land"

    # =========================
    # 상태 업데이트
    # =========================

    def update_state(self):                   
        #보는 방향
        if(abs(self.vx) > 0.1):
            self.dir = numpy.sign(self.vx)

        # 상태 타이머 감소
        if abs(self.temperature) < 1:
            if self.state == "steam":
                self.animestate = "C_con"
                self.movedelay = 36
            elif self.state == "ice":
                self.animestate = "I_unfreeze"
                self.movedelay = 40
                
            self.state = "water"
            
                
        # 애니메이션 상태 전환
        if self.anime_end == True:
            #물 - - - - -
            if self.animestate == "W_walk":
                self.animestate = "W_idle"
                
            elif self.animestate == "W_jump":
                self.animestate = "W_fall"
                
            elif self.animestate == "W_fall":
                self.animestate = "W_falling"
                
            elif self.animestate == "W_land":
                self.animestate = "W_idle"
            #얼음 - - - - -
            elif self.animestate == "W_freeze":
                self.animestate = "I_idle"
                
            elif self.animestate == "I_unfreeze":
                self.animestate = "W_idle"
            #수증기 - - - - -
            elif self.animestate == "W_eva":
                self.animestate = "C_idle"
                
            elif self.animestate == "C_con":
                self.animestate = "W_idle"
                
            self.anime_end = False
            

    # =========================
    # 렌더링
    # =========================

    def draw(self, screen, UIscreen, camera_x, camera_y, WIDTH, HEIGHT):
        target = []
        
        #애니메이션 선택
        #print(self.animestate)
        if self.animestate == "W_idle":
            target = playerW_idle
            self.anime_speed = 24
        elif self.animestate == "W_walk":
            target = playerW_walk
            self.anime_speed = 6
        elif self.animestate == "W_jump":
            target = playerW_jump
            self.anime_speed = 7
            yPivot = 42
        elif self.animestate == "W_fall":
            target = playerW_fall
            self.anime_speed = 7
            yPivot = 42
        elif self.animestate == "W_falling":
            target = playerW_falling
            self.anime_speed = 5
            yPivot = 42
        elif self.animestate == "W_land":
            target = playerW_land
            self.anime_speed = 6
        #얼음
        elif self.animestate == "W_freeze":
            target = playerW_freeze
            self.anime_speed = 6
        elif self.animestate == "I_idle":
            target = playerI_idle
            self.anime_speed = 6
        elif self.animestate == "I_unfreeze":
            target = playerI_unfreeze
            self.anime_speed = 6
        #수증기
        elif self.animestate == "W_eva":
            target = playerW_evaporate
            self.anime_speed = 6
        elif self.animestate == "C_idle":
            target = playerC_idle
            self.anime_speed = 6
        elif self.animestate == "C_con":
            target = playerC_condensation
            self.anime_speed = 6
            
        if self.animestate != self.animestate_pre:
            self.anime_index = 0
            self.anime_timer = 0
            self.anime_end == False
            self.animestate_pre = self.animestate
            
        #애니메이션
        self.anime_timer += 1
        if self.anime_timer >= self.anime_speed:
            self.anime_timer = 0
            self.anime_index = self.anime_index + 1
            
            if self.anime_index == len(target) - 1: #애니메이션 1루프 끝남
                self.anime_end = True
                
            self.anime_index = self.anime_index % len(target)

        img = target[self.anime_index]
        
        if(self.dir == -1): #좌우반전
            img = pygame.transform.flip(img, True, False)
            
        orig_rect = img.get_rect()
        orig_rect.topleft = (int(self.rect.x - camera_x + WIDTH / 2), int(self.rect.y - camera_y + HEIGHT / 2))
            
        if self.state != "steam" and self.land == "slope":
            dx = self.landslope.x2 - self.landslope.x1
            dy = self.landslope.y2 - self.landslope.y1

            angle = math.degrees(math.atan2(dy, dx))
            
            rotated = pygame.transform.rotate(img, -angle)
            
            rot_rect = rotated.get_rect(center=orig_rect.center)

            screen.blit(rotated, rot_rect)
        else:
            screen.blit(img, orig_rect)
        
        #debug_rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)
        
        #pygame.draw.circle(screen, (255,255,0), (self.rect.x, self.rect.y), 4)
        #pygame.draw.rect(screen, (255, 0, 0), debug_rect, 2)
        

        # 온도 게이지
        gauge_image = gauge_sprites[2]
        
        if self.state == "water":
            if abs(self.temperature) < 50: #0근처
                gauge_image = gauge_sprites[2]
            elif numpy.sign(self.temperature) > 0:
                if self.temperature >= 100:
                    gauge_image = gauge_sprites[1]  
                else:
                    gauge_image = gauge_sprites[0]
            else:
                if self.temperature <= -100:
                    gauge_image = gauge_sprites[4]
                else:
                    gauge_image = gauge_sprites[3]
                
        UIscreen.blit(gauge_image, (4, 0))


        gauge_height = (self.temperature + 150) / 300 * 171

        pygame.draw.rect(UIscreen, (255,84,84), (28, 184 - gauge_height, 6, gauge_height))

        # 상태 텍스트
        font = pygame.font.SysFont(None, 32)

        txt = font.render(f"STATE : {self.state}", True, WHITE)

        UIscreen.blit(txt, (80, 20))
