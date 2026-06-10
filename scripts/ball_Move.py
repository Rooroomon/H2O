import pygame, math, numpy

def check_collision(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

class Ball:
    def __init__(self, x, y):
        self.radius = 20
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)

        self.vx = 0
        self.vy = 0

    def update(self, slopes, tilemap, player):
        # 중력
        self.vy += 0.1
        
        self.vy = min(15, self.vy)
        
        prev_rect = self.rect.copy()
        
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        #지형 충돌
        collide_list = check_collision(self.rect, tilemap.wall_rects)
        side = set()
        
        if self.rect.colliderect(player.rect):
            accel = 0
            if self.rect.x < player.rect.x:
                accel = -0.5
            else:
                accel = 0.5
                
            self.vx = player.vx + accel

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
            if self.vx >= 0 and self.rect.x < tile.left - 20 and "right" in side:
                self.vx = 0
                self.rect.right = tile.left
            elif self.vx <= 0 and self.rect.x > tile.right - 8 and "left" in side:
                self.vx = 0
                self.rect.left = tile.right
    
        # 2. 바닥
        self.rect.topleft = (self.rect.x, self.rect.y)
        Yhit_list = check_collision(self.rect, tilemap.wall_rects)
        for tile in Yhit_list:
            if self.vy >= 0 and self.rect.y < tile.top - 20 and "bottom" in side:
                self.vy = 0
                self.rect.bottom = tile.top + 1

        
        # 경사 충돌    
        for slope in slopes:

            if slope.x1 <= self.rect.x <= slope.x2:

                slope_y = slope.get_y(self.rect.x)

                feet = self.rect.y + self.radius

                if feet >= slope_y and feet <= slope_y + 15:

                    self.rect.y = slope_y - self.radius

                    self.vy = 0

                    # 경사 방향 계산
                    dx = slope.x2 - slope.x1
                    dy = slope.y2 - slope.y1

                    angle = math.atan2(dy, dx)

                    # 경사 따라 굴러감
                    self.vx += math.cos(angle) * 0.5 * numpy.sign(angle)

        # 마찰
        self.vx *= 0.99

    def draw(self, screen, camera_x, camera_y, WIDTH, HEIGHT):

        pygame.draw.circle(
            screen,
            (255, 200, 100),
            (self.rect.x - camera_x + WIDTH / 2 + self.radius, self.rect.y - camera_y + HEIGHT / 2 + self.radius),
            self.radius
        )