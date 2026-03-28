import pygame
pygame.init()

# constantes
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

def load_spritesheet(path, cols=2, rows=2):
    spritesheet = pygame.image.load(path).convert_alpha()
    frame_width = spritesheet.get_width() // cols
    frame_height = spritesheet.get_height() // rows
    frames = []
    for row in range(rows):
        for col in range(cols):
            frame = spritesheet.subsurface((col * frame_width, row * frame_height, frame_width, frame_height))
            frames.append(frame)
    return frames


class Game:
    def __init__(self):
        self.bg = pygame.image.load("bg.jpg").convert()
        self.player = Player()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.xp = 0
        self.velocity = 2

        # paliers d'xp
        self.xp_thresholds = [0, 10, 25]
        self.current_level = 0

        # charger les 3 apparences
        self.all_animations = []
        for i in range(1, 4):
            self.all_animations.append({
                "left": load_spritesheet(f"Player_left_{i}.png"),
                "right": load_spritesheet(f"Player_right_{i}.png"),
            })

        self.animations = self.all_animations[0]
        self.direction = "left"
        self.current_frame = 0
        self.animation_speed = 150
        self.last_update = pygame.time.get_ticks()
        self.is_moving = False

        self.image = self.animations[self.direction][0]
        self.rect = self.image.get_rect(x=0, y=0)

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

    def handle_input(self, pressed):
        self.is_moving = False

        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.rect.x += self.velocity
            self.direction = "right"
            self.is_moving = True
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            self.rect.x -= self.velocity
            self.direction = "left"
            self.is_moving = True
        if pressed[pygame.K_UP] or pressed[pygame.K_z]:
            self.rect.y -= self.velocity
            self.is_moving = True
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.rect.y += self.velocity
            self.is_moving = True

        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

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


# --- Lancement ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Player")
clock = pygame.time.Clock()
game = Game()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                game.player.gain_xp(5)
                print(f"XP: {game.player.xp} | Niveau: {game.player.current_level + 1}")

    game.player.handle_input(pygame.key.get_pressed())
    game.player.animate()

    screen.blit(game.bg, (0, 0))
    screen.blit(game.player.image, game.player.rect)
    pygame.display.flip()

pygame.quit()