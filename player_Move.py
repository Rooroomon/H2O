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
gaugeDot_sprite = pygame.transform.scale(pygame.image.load("./assets/Sprite/Gauge_Dot.png"), (39, 30))


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
    player_frames.append(player_sheet.subsurface(rect))
    
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

gauge_sprites.append(pygame.transform.scale(gauge_sheet.subsurface((0, 0, 77, 14)), (231, 42)))
gauge_sprites.append(pygame.transform.scale(gauge_sheet.subsurface((0, 14, 77, 14)), (231, 42)))
gauge_sprites.append(pygame.transform.scale(gauge_sheet.subsurface((0, 28, 77, 14)), (231, 42)))

clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x = 100
        self.y = 500

        self.vx = 0
        self.vy = 0

        self.width = 56
        self.height = 56
        
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
    # 상태 변경
    # =========================

    def set_state(self, new_state):
        self.state = new_state

    # =========================
    # 입력 처리
    # =========================

    def input(self):
        keys = pygame.key.get_pressed()
        
        if self.transCool < 0 and keys[pygame.K_f]:            
            if self.state == "water":
                if self.temperature >= 100:
                    self.set_state("steam")
                    self.movedelay = 36
                    self.animestate = "W_eva"
                    self.transCool = 60
                elif self.temperature <= -100:
                    self.set_state("ice")
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
                    
                self.set_state("water")
                
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
                speed = 4
    
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.vx = -speed
                    if self.on_ground:
                        self.animestate = "W_walk"
                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.vx = speed
                    if self.on_ground:
                        self.animestate = "W_walk"
                else:
                    self.vx *= 0.6
    
                # 점프
                if keys[pygame.K_SPACE] and self.on_ground:
                    self.vy = -7
                    self.animestate = "W_jump"
    
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

    # =========================
    # 물리
    # =========================

    def physics(self, platforms, slopes):
        dt = clock.tick(60) / 1000
        self.temp_clock += dt
        
        
        if self.state != "water":
            self.temperature -= numpy.sign(self.temperature) * dt * 25
        elif self.temp_clock > 4:
            self.temperature -= numpy.sign(self.temperature) * dt * 7.5
            if abs(self.temperature) < 2:
                self.temp_clock = -500
                
        self.temperature = max(-150, min(self.temperature, 150))
                

        # 중력
        if self.state != "steam":
            self.vy += 0.25

        self.x += self.vx
        self.y += self.vy

        self.on_ground = False

        player_rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

        for p in platforms:

            if player_rect.colliderect(p):

                # 아래에서 착지
                if self.vy > 0:
                    self.land = "ground"
                    
                    self.y = p.y - self.height
                    self.vy = 0
                    self.on_ground = True
                    if self.animestate == "W_fall" or self.animestate == "W_falling":
                        self.animestate = "W_land"
                        
            
        for slope in slopes:

            if slope.x1 <= self.x + self.width/2 <= slope.x2:

                slope_y = slope.get_y(self.x + self.width/2)

                feet = self.y + self.height

                # 경사 위에 착지
                if feet >= slope_y - 5 and feet <= slope_y + 25 and self.vy >= 0:
                    self.land = "slope"
                    self.landslope = slope

                    self.y = slope_y - self.height
                    self.vy = 0
                    self.on_ground = True
                    if self.animestate == "W_fall" or self.animestate == "W_falling":
                        self.animestate = "W_land"
                        
        if self.on_ground == False:
            self.land = "none"

    # =========================
    # 상태 업데이트
    # =========================

    def update_state(self):                   
        #보는 방향
        if(abs(self.vx) > 0.1):
            self.dir = numpy.sign(self.vx)

        # 상태 타이머 감소
        if abs(self.temperature) < 2:
            if self.state == "steam":
                self.animestate = "C_con"
                self.movedelay = 36
            elif self.state == "ice":
                self.animestate = "I_unfreeze"
                self.movedelay = 40
                
            self.set_state("water")
            
                
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

    def draw(self, screen, UIscreen):
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
            self.anime_speed = 6
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
            self.animestate_pre = self.animestate
            self.anime_end == False
            
        #애니메이션
        self.anime_timer += 1
        if self.anime_timer >= self.anime_speed:
            self.anime_timer = 0
            self.anime_index = self.anime_index + 1
            
            if self.anime_index == len(target) - 1: #애니메이션 1루프 끝남
                self.anime_end = True
                
            self.anime_index = self.anime_index % len(target)

        img = target[self.anime_index]
        img = pygame.transform.scale(img, (self.width, self.height))
        
        if(self.dir == -1): #좌우반전
            img = pygame.transform.flip(img, True, False)
            
        orig_rect = img.get_rect()
        orig_rect.topleft = (self.x, self.y)            
            
        if self.state != "steam" and self.land == "slope":
            dx = self.landslope.x2 - self.landslope.x1
            dy = self.landslope.y2 - self.landslope.y1

            angle = math.degrees(math.atan2(dy, dx))
            
            rotated = pygame.transform.rotate(img, -angle)
            
            rot_rect = rotated.get_rect(center=orig_rect.center)

            screen.blit(rotated, rot_rect)
        else:
            screen.blit(img, orig_rect)
        
        #debug_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        #pygame.draw.circle(screen, (255,255,0), (self.x, self.y), 4)
        #pygame.draw.rect(screen, (255, 0, 0), debug_rect, 2)
        

        # 온도 게이지
        if self.temperature <= -100:
            UIscreen.blit(gauge_sprites[1], (0, 0))
        elif self.temperature >= 100:
            UIscreen.blit(gauge_sprites[2], (0, 0))
        else:
            UIscreen.blit(gauge_sprites[0], (0, 0))

        center = 115.5

        gauge_x = center + self.temperature * 0.6 - 19.5

        UIscreen.blit(gaugeDot_sprite, (gauge_x, 6))

        # 상태 텍스트
        font = pygame.font.SysFont(None, 32)

        txt = font.render(f"STATE : {self.state}", True, WHITE)

        UIscreen.blit(txt, (20, 60))
