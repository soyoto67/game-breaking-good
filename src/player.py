import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITES_DIR = os.path.join(BASE_DIR, '..', 'assets', 'sprites', 'player')

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60


def load_spritesheet(path, cols=2, rows=2, scale=0.4):
    spritesheet = pygame.image.load(path).convert_alpha()
    frame_width = spritesheet.get_width() // cols
    frame_height = spritesheet.get_height() // rows
    frames = []
    for row in range(rows):
        for col in range(cols):
            frame = spritesheet.subsurface((col * frame_width, row * frame_height, frame_width, frame_height))
            new_w = int(frame_width * scale)
            new_h = int(frame_height * scale)
            frame = pygame.transform.scale(frame, (new_w, new_h))
            frames.append(frame)
    return frames


class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.xp = 0
        self.velocity = 2.5

        self.xp_thresholds = [0, 10, 25]
        self.current_level = 0

        self.all_animations = []
        for i in range(1, 4):
            self.all_animations.append({
                "left": load_spritesheet(os.path.join(SPRITES_DIR, f"Player_left_{i}.png"), scale=0.4),
                "right": load_spritesheet(os.path.join(SPRITES_DIR, f"Player_right_{i}.png"), scale=0.4),
            })

        self.animations = self.all_animations[0]
        self.direction = "left"
        self.current_frame = 0
        self.animation_speed = 150
        self.last_update = pygame.time.get_ticks()
        self.is_moving = False

        self.image = self.animations[self.direction][0]
        self.rect = self.image.get_rect(x=x, y=y)
        self.pos_x = float(x)
        self.pos_y = float(y)

    def update(self):
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

    def gain_xp(self, amount):
        self.xp += amount
        new_level = self.current_level
        for i, threshold in enumerate(self.xp_thresholds):
            if self.xp >= threshold:
                new_level = i
        if new_level != self.current_level:
            self.current_level = new_level
            self.animations = self.all_animations[new_level]
            self.current_frame = 0

    def handle_input(self, pressed, walls=[]):
        self.is_moving = False
        old_x = self.pos_x
        old_y = self.pos_y

        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.pos_x += self.velocity
            self.direction = "right"
            self.is_moving = True
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            self.pos_x -= self.velocity
            self.direction = "left"
            self.is_moving = True
        if pressed[pygame.K_UP] or pressed[pygame.K_z]:
            self.pos_y -= self.velocity
            self.is_moving = True
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.pos_y += self.velocity
            self.is_moving = True

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        feet_rect = pygame.Rect(
            self.rect.x + self.rect.width // 4,
            self.rect.y + self.rect.height * 3 // 4,
            self.rect.width // 2,
            self.rect.height // 4
        )

        for wall in walls:
            if feet_rect.colliderect(wall):
                self.pos_x = old_x
                self.pos_y = old_y
                self.rect.x = int(self.pos_x)
                self.rect.y = int(self.pos_y)
                self.is_moving = False
                break

    def animate(self):
        frames = self.animations[self.direction]
        if self.is_moving:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(frames)
        else:
            self.current_frame = 0
        self.image = frames[self.current_frame]


if __name__ == '__main__':
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Player")
    clock = pygame.time.Clock()
    player = Player()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    player.gain_xp(5)
                    print(f"XP: {player.xp} | Niveau: {player.current_level + 1}")

        player.handle_input(pygame.key.get_pressed())
        player.animate()
        player.update()

        screen.fill((0, 0, 0))
        screen.blit(player.image, player.rect)
        pygame.display.flip()

    pygame.quit()