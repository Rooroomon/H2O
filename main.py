import pygame, math, numpy

pygame.init()

# =========================
# 파일 로드
# =========================
icon = pygame.image.load("./assets/Sprite/Icon.png")
player_sheet = pygame.image.load("./assets/Sprite/Player_Sheet.png")
gauge_image = pygame.image.load("./assets/Sprite/Gauge.png")

player_frames = []
FRAME_W, FRAME_H = 16, 16
COLS = 11

for i in range(165):
    row, col = divmod(i, COLS)
    rect = pygame.Rect(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
    player_frames.append(player_sheet.subsurface(rect))

playerW_idle = [player_frames[i] for i in [0, 1]]
playerW_walk = [player_frames[i] for i in [11, 12, 13, 14, 15]]
playerW_jump = [player_frames[i] for i in [22, 23, 24 ,25, 26]]
playerW_fall = [player_frames[i] for i in [33, 34, 35, 36]]
playerW_falling = [player_frames[i] for i in [36]]
playerW_land = [player_frames[i] for i in [44, 45, 46, 47]]
playerW_freeze = [player_frames[i] for i in [55, 56, 57, 58, 59, 66, 67, 68, 69]]
playerW_evaporate = [player_frames[i] for i in [110, 111, 112, 113, 121, 122 ,123, 124]]

playerI_idle = [player_frames[i] for i in [77]]
playerI_unfreeze = [player_frames[i] for i in [88, 89, 90, 91, 92, 99, 100, 101, 102]]

playerC_idle = [player_frames[i] for i in [132]]
playerC_condensation = [player_frames[i] for i in [143, 144, 145, 146, 154, 155, 156, 157]]


# =========================
# 설정
# =========================

WIDTH, HEIGHT = 1080, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("H2O")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

#전체화면 테스트 - - - - - - - - - - - - - - -
# 모니터 해상도 가져오기 (전체화면용)
#info = pygame.display.Info()
#screen_w, screen_h = info.current_w, info.current_h

# 전체화면 플래그와 함께 화면 설정
#screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
# -------------------------------

# =========================
# 색상
# =========================

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)

BLUE = (80, 140, 255)
ICE = (180, 240, 255)
STEAM = (220, 220, 220)

RED = (255, 100, 100)
CYAN = (100, 255, 255)

GROUND = (90, 90, 90)

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
                player.temperature += 0.75
            else:
                player.temperature -= 0.75
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
            (self.x1, self.y1 + 6),
            (self.x2, self.y2 + 6),
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

        # 바닥 충돌
        for p in platforms:

            rect = pygame.Rect(
                self.x - self.radius,
                self.y - self.radius,
                self.radius * 2,
                self.radius * 2
            )

            if rect.colliderect(p):

                self.y = p.y - self.radius
                self.vy = 0

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

        if new_state in ["ice", "steam"]:
            self.state_timer = 600  # 10초
        else:
            self.state_timer = 0

    # =========================
    # 입력 처리
    # =========================

    def input(self):
        keys = pygame.key.get_pressed()
        
        if(self.movedelay > 0):
            self.movedelay -= 1
        else:
            # ---------------------
            # 물
            # ---------------------
            if self.state == "water":
                speed = 5
    
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.vx = -speed
                    if self.on_ground:
                        self.animestate = "W_walk"
                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.vx = speed
                    if self.on_ground:
                        self.animestate = "W_walk"
                else:
                    self.vx *= 0.75
    
                # 점프
                if keys[pygame.K_SPACE] and self.on_ground:
                    self.vy = -10
                    self.animestate = "W_jump"
    
            # ---------------------
            # 얼음
            # ---------------------
            elif self.state == "ice":
                accel = 0.3
                max_speed = 8
    
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
                max_speed = 5
    
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

    def physics(self):
        dt = clock.tick(60) / 1000
        self.temp_clock += dt
        
        
        if self.state != "water":
            self.temperature -= numpy.sign(self.temperature) * dt * 25
        elif self.temp_clock > 10:
            self.temperature -= numpy.sign(self.temperature) * dt * 5
            if abs(self.temperature) < 2:
                self.temp_clock = -500
                

        # 중력
        if self.state != "steam":
            self.vy += 0.5

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

        # 화면 밖 제한
        if self.x < 0:
            self.x = 0

        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width

        if self.y > HEIGHT:
            self.x = 100
            self.y = 100
            
        for slope in slopes:

            if slope.x1 <= self.x + self.width/2 <= slope.x2:

                slope_y = slope.get_y(self.x + self.width/2)

                feet = self.y + self.height

                # 경사 위에 착지
                if feet >= slope_y and feet <= slope_y + 20:
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
        if(abs(self.vx) > 0.1):
            self.dir = numpy.sign(self.vx)
        
        for event in pygame.event.get():
            # 키 눌림 체크
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if self.state == "water":
                        if self.temperature >= 100:
                            self.set_state("steam")
                            self.movedelay = 36
                            self.animestate = "W_eva"
                        elif self.temperature <= -100:
                            self.set_state("ice")
                            self.movedelay = 40
                            self.animestate = "W_freeze"
                    else:
                        if self.state == "steam":
                            self.animestate = "C_con"
                            self.movedelay = 36
                        elif self.state == "ice":
                            self.animestate = "I_unfreeze"
                            self.movedelay = 40
                            
                        self.set_state("water")


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

    def draw(self, screen):
        target = []
        xPivot = 56
        yPivot = 56
        
        #애니메이션 선택
        #print(self.animestate)
        if self.animestate == "W_idle":
            target = playerW_idle
            self.anime_speed = 12
        elif self.animestate == "W_walk":
            target = playerW_walk
            self.anime_speed = 4
        elif self.animestate == "W_jump":
            target = playerW_jump
            self.anime_speed = 5
            yPivot = 42
        elif self.animestate == "W_fall":
            target = playerW_fall
            self.anime_speed = 4
            yPivot = 42
        elif self.animestate == "W_falling":
            target = playerW_falling
            self.anime_speed = 4
            yPivot = 42
        elif self.animestate == "W_land":
            target = playerW_land
            self.anime_speed = 4
        #얼음
        elif self.animestate == "W_freeze":
            target = playerW_freeze
            self.anime_speed = 4
        elif self.animestate == "I_idle":
            target = playerI_idle
            self.anime_speed = 4
        elif self.animestate == "I_unfreeze":
            target = playerI_unfreeze
            self.anime_speed = 4
        #수증기
        elif self.animestate == "W_eva":
            target = playerW_evaporate
            self.anime_speed = 4
        elif self.animestate == "C_idle":
            target = playerC_idle
            self.anime_speed = 4
        elif self.animestate == "C_con":
            target = playerC_condensation
            self.anime_speed = 4
            
        if self.animestate != self.animestate_pre:
            self.anime_index = 0
            self.anime_timer = 0
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
        img = pygame.transform.scale(img, (self.width, self.height))
        
        if(self.dir == -1): #좌우반전
            img = pygame.transform.flip(img, True, False)
            
        orig_rect = img.get_rect()
        orig_rect.topleft = (self.x, self.y)            
            
        if self.land == "slope":
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
        pygame.draw.rect(screen, WHITE, (20, 20, 200, 20), 2)

        center = 120

        gauge_x = center + self.temperature * 0.6

        gauge_x = max(20, min(220, gauge_x))

        color = RED if self.temperature > 0 else CYAN

        pygame.draw.circle(screen, color, (int(gauge_x), 30), 8)

        # 상태 텍스트
        font = pygame.font.SysFont(None, 32)

        txt = font.render(f"STATE : {self.state}", True, WHITE)

        screen.blit(txt, (20, 60))


player = Player()

# ==================================================
# 맵
# ==================================================

platforms = [
    pygame.Rect(0, 650, 1200, 50),
    pygame.Rect(350, 500, 350, 30),
    pygame.Rect(700, 400, 250, 30),
]

slopes = [
    Slope(200, 600, 500, 450),
    Slope(700, 500, 1000, 600),
]

balls = [
    Ball(300, 100, 20)
]
# =========================
# 메인 루프
# =========================

running = True

while running:

    dt = clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # =====================
    # 업데이트
    # =====================

    player.input()

    for obj in objects:
        obj.affect_player(player)

    player.physics()

    player.update_state()
    
    for ball in balls:
        ball.update()


    # =====================
    # 렌더링
    # =====================

    screen.fill(BLACK)

    # 발판
    for p in platforms:
        pygame.draw.rect(screen, GROUND, p)

    # 오브젝트
    for obj in objects:
        obj.draw(screen)

    # 플레이어
    player.draw(screen)
    
    for slope in slopes:
        slope.draw(screen)

    for ball in balls:
        ball.draw(screen)

    pygame.display.flip()

pygame.quit()