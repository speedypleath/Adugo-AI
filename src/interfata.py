import pygame
import pygame_menu
import sys
import os
class Interfata:
    play_menu = None
    def __init__(self):
        print("init")
        pygame.init()
        pygame.display.init()
        pygame.display.set_mode((1,1))
        pygame.display.set_caption("Adugo")
        self.padding_x = 50
        self.padding_y = 30
        self.nr_coloane = 4
        self.nr_linii = 6
        self.width = 100
        script_dir = sys.path[0]
        img_path = os.path.join(script_dir, '../assets/dog.png')
        self.dog_img = pygame.image.load(img_path)
        self.dog_img = pygame.transform.scale(self.dog_img, (100, 60))
        img_path = os.path.join(script_dir, '../assets/jaguar.png')
        self.jaguar_img = pygame.image.load(img_path)
        self.jaguar_img = pygame.transform.scale(self.jaguar_img, (100, 60))
        self.ecran = pygame.display.set_mode(
            size=(2 * self.padding_x + self.nr_coloane * self.width, 2 * self.padding_y + self.nr_linii * self.width))  # N *w+ N-1= N*(w+1)-1
        self.celule_grid = []
        for linie in range(0, 5):
            for coloana in range(0, 5):
                patr = pygame.Rect(coloana*(self.width+1), linie*(self.width+1), self.width, self.width)
                self.celule_grid.append(patr)
        for coloana in range(1, 4):
            patr = pygame.Rect(coloana*(self.width+1), 5*(self.width+1), self.width, self.width)
            self.celule_grid.append(patr)
        for coloana in range(0, 5, 2):
            patr = pygame.Rect(coloana*(self.width+1), 6*(self.width+1), self.width, self.width)
            self.celule_grid.append(patr)

    def empty_grid(self):
        self.ecran.fill((255, 255, 255))
        for i in range(0, 500, 100):
            pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x, self.padding_y + i),
                             (self.padding_x + self.nr_coloane * self.width, self.padding_y + i), 7)
            pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x + i, self.padding_y),
                             (self.padding_x + i, self.padding_y + self.nr_coloane * self.width), 7)
        pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x, self.padding_y),
                         (self.padding_x + self.nr_coloane * self.width, self.padding_y + self.nr_coloane * self.width), 9)
        pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x + self.nr_coloane * self.width, self.padding_y),
                         (self.padding_x, self.padding_y + self.nr_coloane * self.width), 9)
        pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x + 2 * self.width, self.padding_y),
                         (self.padding_x + 4 * self.width, self.padding_y + 2 * self.width), 9)
        pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x, self.padding_y + 2 * self.width),
                         (self.padding_x + 2 * self.width, self.padding_y + 4 * self.width), 9)
        pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x + 4 * self.width, self.padding_y + 2 * self.width),
                         (self.padding_x + 2 * self.width, self.padding_y + 4 * self.width), 9)
        pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x + 2 * self.width, self.padding_y),
                         (self.padding_x, self.padding_y + 2 * self.width), 9)

        pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x + 2 * self.width, self.padding_y + 4 * self.width),
                         (self.padding_x, self.padding_y + 6 * self.width), 9)
        pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x + 2 * self.width, self.padding_y + 4 * self.width),
                         (self.padding_x + 2 * self.width, self.padding_y + 6 * self.width), 7)
        pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x + 2 * self.width, self.padding_y + 4 * self.width),
                         (self.padding_x + 4 * self.width, self.padding_y + 6 * self.width), 9)
        pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x + 1 * self.width, self.padding_y + 5 * self.width),
                         (self.padding_x + 3 * self.width, self.padding_y + 5 * self.width), 7)
        pygame.draw.line(self.ecran, (0, 0, 0), (self.padding_x, self.padding_y + 6 * self.width),
                         (self.padding_x + 4 * self.width, self.padding_y + 6 * self.width), 7)
     
    def stare_initiala(self):
        self.empty_grid()
        for i in range(0, 500, 100):
            for j in range(0, 300, 100):
                self.ecran.blit(self.dog_img, (i, j))

        self.ecran.blit(self.jaguar_img, (200, 200))
        pygame.display.update()


    def meniu(self, joc):
        if self.play_menu is None:
            self.play_menu = pygame_menu.Menu(
                    height = (2 * self.padding_x + self.nr_coloane * self.width) * 0.75,
                    title = 'Play Menu',
                    width = (2 * self.padding_y + self.nr_linii * self.width) * 0.7
                )
            self.play_menu.add.selector('Difficulty ',
                                [('Easy', 1),
                                ('Medium', 2),
                                ('Hard', 3)],
                                onchange=joc.change_difficulty,
                                selector_id='select_difficulty')
            self.play_menu.add.selector('Player ',
                                [('Jaguar', 'JAGUAR'),
                                ('Dog', 'CAINE')],
                                onchange=joc.change_player,
                                selector_id='select_player')
            self.play_menu.add.selector('Algorithm ',
                                [('Minimax', 'Minimax'),
                                ('Alphabeta', 'Alphabeta')],
                                onchange=joc.change_algorithm,
                                selector_id='select_algorithm')
            self.play_menu.add.selector('Mode ',
                                [('Player vs Player', 'PVP'),
                                ('Player vs Comp', 'PVE'),
                                ('Comp vs Comp', 'AI')],
                                onchange=joc.change_type,
                                selector_id='select_type')
            
            self.play_menu.add.button('Play', self.play_menu.disable)
            self.play_menu.mainloop(self.ecran)
        else:
            self.play_menu.full_reset()
            self.play_menu.enable()
            self.play_menu.mainloop(self.ecran)
            
    def end_game(self, winner):
        end_menu = pygame_menu.Menu(
                    height = (2 * self.padding_x + self.nr_coloane * self.width) * 0.75,
                    title = winner,
                    width = (2 * self.padding_y + self.nr_linii * self.width) * 0.7
                )
        end_menu.add.button('Play again', end_menu.disable)
        end_menu.mainloop(self.ecran)

    
    def update_board(self, tabla):
        print("update board")
        self.empty_grid()
        for x in tabla.nodes:
            if x is not None:
                if x.value == '0':
                    self.ecran.blit(self.dog_img, (x.y_value * self.width, x.x_value * self.width));
                elif x.value == '1':
                    print(x.x_value, x.y_value)
                    self.ecran.blit(self.jaguar_img, (x.y_value * self.width, x.x_value * self.width));
        pygame.display.update()
        
    def markup(self, nod):
        surface = pygame.Surface((40,40))
        surface.set_colorkey((0,0,0)) 
        surface.set_alpha(128) 
        pygame.draw.circle(surface, (0,255,0), (20,20), 20)
        self.ecran.blit(surface, (nod.y_value * self.width + self.padding_x - 20, nod.x_value * self.width + self.padding_y - 20))
        pygame.display.update()