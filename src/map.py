import pygame
import pytmx
import pyscroll
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from player import Player

class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Breaking Good")

        BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'maps')
        tmx_data = pytmx.util_pygame.load_pygame(os.path.join(BASE_DIR, "breaking_good_map.tmx"))
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)

        try:
            player_start = tmx_data.get_object_by_name("player")
            start_x = player_start.x
            start_y = player_start.y
        except KeyError:
            start_x, start_y = 200, 300

        self.player = Player(start_x, start_y)

        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision" or obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        print(f"Murs détectés : {len(self.walls)}")

        self.group.add(self.player)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.player.handle_input(pygame.key.get_pressed(), self.walls)
            self.player.animate()

            self.group.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

        pygame.quit()