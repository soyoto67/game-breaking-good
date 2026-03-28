import pygame
import pytmx
import pyscroll
from player import Player
class Game:

    def __init__(self):



        #creation de la fenetre du jeu 
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("breaking-good")

        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('breaking_good_map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3.5


        #generer un joueur
        player_position = tmx_data.get_object_by_name("spawn")
        self.player = Player(player_position.x , player_position.y)

        #definir une liste qui va contenir les obstacles
        self.walls = [] 

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.rect(obj.x, obj.y, obj.width, obj.height ))
        

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        self.group.add(self.player)
        # intro du jeu
        self.intro = True
        self.intro_timer = 0
    
    def play_intro(self, dt):
        self.intro_timer += dt

        # Le joueur marche tout seul pendant 2 secondes
        if self.intro_timer < 2000:
            self.player.rect.y += 2

        # Quand l’intro est finie
        if self.intro_timer > 2000:
            self.intro = False


    def run(self):

        # la boucle du jeu
        running = True

        while running:
                
            dt = pygame.time.Clock().tick(60)  # pour mesurer le temps

            if self.intro:
                self.play_intro(dt)
            else:
                self.group.update()


            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()