import pygame, math, numpy

font = pygame.font.Font("./assets/NeoDunggeunmo.ttf", 40)
GRAY = (161, 161, 161)
clock = pygame.time.Clock()
start_text = font.render("게임 시작", True, (0, 0, 0))
quit_text = font.render("종료", True, (0, 0, 0))

class Menu:
    def __init__(self, WIDTH, HEIGHT):
        self.title_sheet = pygame.image.load("./assets/Sprite/Title_Sheet.png").convert_alpha()
        self.button_sheet = pygame.image.load("./assets/Sprite/Title_Button.png").convert_alpha()

        self.title_sprites = [self.title_sheet.subsurface((0, 0, 176, 88)), self.title_sheet.subsurface((0, 88, 176, 88))]
        self.button_sprites = [self.button_sheet.subsurface((0, 0, 40, 16)), self.button_sheet.subsurface((0, 16, 40, 16))]

        self.scaled_sprites = []
        self.scaledbutton_sprites = []
        
        self.scale = min(WIDTH/176, HEIGHT/88)
        
        self.scaled_sprites.append(pygame.transform.scale(self.title_sprites[0], (int(176 * self.scale), int(88 * self.scale))))
        self.scaled_sprites.append(pygame.transform.scale(self.title_sprites[1], (int(176 * self.scale), int(88 * self.scale))))
        self.scaledbutton_sprites.append(pygame.transform.scale(self.button_sprites[0], (int(40 * self.scale), int(16 * self.scale))))
        self.scaledbutton_sprites.append(pygame.transform.scale(self.button_sprites[1], (int(40 * self.scale), int(16 * self.scale))))
        
        
        self.startbutton_rect = pygame.Rect(WIDTH * 0.6, HEIGHT * 0.5, int(40 * self.scale), int(16 * self.scale))
        self.quitbutton_rect = pygame.Rect(WIDTH * 0.6, HEIGHT * 0.7, int(40 * self.scale), int(16 * self.scale))
        
        self.startbutton_sprite = self.scaledbutton_sprites[0]
        self.quitbutton_sprite = self.scaledbutton_sprites[0]
        
    def change_scale(self, WIDTH, HEIGHT):
        self.scale = min(WIDTH/176, HEIGHT/88)
        
        self.scaled_sprites[0] = pygame.transform.scale(self.title_sprites[0], (int(176 * self.scale), int(88 * self.scale)))
        self.scaled_sprites[1] = pygame.transform.scale(self.title_sprites[1], (int(176 * self.scale), int(88 * self.scale)))
        self.scaledbutton_sprites[0] = pygame.transform.scale(self.button_sprites[0], (int(40 * self.scale), int(16 * self.scale)))
        self.scaledbutton_sprites[1] = pygame.transform.scale(self.button_sprites[1], (int(40 * self.scale), int(16 * self.scale)))
        
        self.startbutton_rect = pygame.Rect(WIDTH * 0.6, HEIGHT * 0.5, int(40 * self.scale), int(16 * self.scale))
        self.quitbutton_rect = pygame.Rect(WIDTH * 0.6, HEIGHT * 0.7, int(40 * self.scale), int(16 * self.scale))
        
        self.startbutton_sprite = self.scaledbutton_sprites[0]
        self.quitbutton_sprite = self.scaledbutton_sprites[0]
        
    def menu_button(self, event):
        # 마우스 클릭
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 왼쪽 버튼
                if self.startbutton_rect.collidepoint(event.pos):
                    self.startbutton_sprite = self.scaledbutton_sprites[1]
                    return "None"
                elif self.quitbutton_rect.collidepoint(event.pos):
                    self.quitbutton_sprite = self.scaledbutton_sprites[1]
                    return "None"
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 왼쪽 버튼
                if self.startbutton_rect.collidepoint(event.pos):
                    self.startbutton_sprite = self.scaledbutton_sprites[0]
                    return "start"
                elif self.quitbutton_rect.collidepoint(event.pos):
                    self.quitbutton_sprite = self.scaledbutton_sprites[0]
                    return "quit"
        
        self.startbutton_sprite = self.scaledbutton_sprites[0]
        self.quitbutton_sprite = self.scaledbutton_sprites[0]
        return "None"
    
    def draw(self, screen, WIDTH, HEIGHT):
        img = self.scaled_sprites[0] if (pygame.time.get_ticks() // 600) % 2 == 0 else self.scaled_sprites[1]
        
        screen.blit(img, ((WIDTH - 176 * self.scale)/2, (HEIGHT - 88 * self.scale)/2))

        # 버튼 그리기
        screen.blit(self.startbutton_sprite, self.startbutton_rect)
        screen.blit(start_text, start_text.get_rect(center=self.startbutton_rect.center))
        
        screen.blit(self.quitbutton_sprite, self.quitbutton_rect)
        screen.blit(quit_text, quit_text.get_rect(center=self.quitbutton_rect.center))
