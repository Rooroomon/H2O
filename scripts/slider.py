import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Slider:
    def __init__(self, x, y, width, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, width, 6)

        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val

        handle_x = x + (start_val - min_val) / (max_val - min_val) * width
        self.handle = pygame.Rect(handle_x - 10, y - 7, 20, 20)

        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.handle.centerx = event.pos[0]

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle.centerx = max(
                self.rect.left,
                min(event.pos[0], self.rect.right)
            )

            ratio = (self.handle.centerx - self.rect.left) / self.rect.width
            self.value = self.min_val + ratio * (self.max_val - self.min_val)

    def draw(self, surface):
        pygame.draw.rect(surface, (180, 180, 180), self.rect)
        pygame.draw.circle(surface, (50, 120, 255), self.handle.center, 6)

slider = Slider(100, 250, 60, 0, 1, 0.5)

font = pygame.font.SysFont(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        slider.handle_event(event)

    screen.fill((30, 30, 30))

    slider.draw(screen)

    text = font.render(
        f"Value: {slider.value:.2f}",
        True,
        (255, 255, 255)
    )
    screen.blit(text, (100, 200))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()