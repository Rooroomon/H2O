import pygame

clock = pygame.time.Clock()

class Slider:
    def __init__(self, x, y, width, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, width, 8)
        
        self.sheet = pygame.image.load("./assets/Sprite/Speaker_Sheet.png")
        self.sprites = []

        self.sprites.append(pygame.transform.scale(self.sheet.subsurface((0, 0, 16, 16)), (width, width)))
        self.sprites.append(pygame.transform.scale(self.sheet.subsurface((16, 0, 16, 16)), (width, width)))
        self.sprites.append(pygame.transform.scale(self.sheet.subsurface((32, 0, 16, 16)), (width, width)))
        self.sprites.append(pygame.transform.scale(self.sheet.subsurface((48, 0, 16, 16)), (width, width)))

        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val

        handle_x = x + (start_val - min_val) / (max_val - min_val) * width
        self.handle = pygame.Rect(handle_x - 10, y - 7, 20, 20)

        self.dragging = False

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    self.handle.centerx = event.pos[0]
                    
                    ratio = (self.handle.centerx - self.rect.left) / self.rect.width
                    self.value = self.min_val + ratio * (self.max_val - self.min_val)
    
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
    
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.handle.centerx = max(
                    self.rect.left,
                    min(event.pos[0], self.rect.right)
                )
    
                ratio = (self.handle.centerx - self.rect.left) / self.rect.width
                self.value = self.min_val + ratio * (self.max_val - self.min_val)
            else:
                self.handle.centerx = self.rect.left + self.value * self.rect.width
                self.handle.y = self.rect.y - 7
            
        return self.value

    def draw(self, surface):
        index = 0
        if self.value > 0.66:
            index = 3
        elif self.value > 0.33:
            index = 2
        elif self.value > 0:
            index = 1

        surface.blit(self.sprites[index], (self.rect.x, self.rect.y - self.rect.width))
        pygame.draw.rect(surface, (225, 225, 225), self.rect)
        pygame.draw.circle(surface, (50, 120, 255), self.handle.center, 6)