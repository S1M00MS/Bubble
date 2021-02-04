import pygame, os, random, time
pygame.init()

class Settings(object):
    width = 800
    height = 800
    fps = 60       
    title = "Bubble" 
    file_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "imagesbubble")
    bordersize = 10
    score = 0

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)



class Bubble(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "bubble.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (5,5))
        self.rect = self.image.get_rect()
        self.rect.centerx = (Settings.width - self.rect.width) // 2
        self.rect.centery = (Settings.height - self.rect.height) // 2
        self.radius = random.randrange(1,5)
        self.starttime = time.time()

    def update(self):
        if (time.time() - self.starttime) >= 1:
            self.image = pygame.transform.scale(self.image, (5+self.radius,5+self.radius))
            self.starttime = time.time()

class Maus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "maus.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,25))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.left = pygame.mouse.get_pos() [0]
        self.rect.bottom = pygame.mouse.get_pos() [1]

class Pause():
    def __init__(self):
        pass

class Endscreen():
    def __init__(self):
        pass

class save_score():
    def __init__(self):
        self.datei_name = ('Score.txt')
        self.text = Settings.score

    def ausgabe(self):
        file = open(self.datei_name,'a')
        file.write(self.text+ '\n')

class Game():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.done = False
        self.screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption(Settings.title)
        #Background erstellen
        self.background = pygame.image.load(os.path.join(Settings.images_path, "background.png")).convert()
        self.background = pygame.transform.scale(self.background, (Settings.width, Settings.height))
        self.background_rect = self.background.get_rect()

        #sprites
        self.all_bubbles = pygame.sprite.Group()
        self.bubble = Bubble()
        self.all_bubbles.add(self.bubble)

        self.all_maus = pygame.sprite.Group()
        self.maus = Maus()
        self.all_maus.add(self.maus)

        #score
        self.score = pygame.font.SysFont("Arial", 20, True, False)
        self.color = (0, 0, 0)

        pygame.mouse.set_visible(False)
    
    def show(self):
        self.screen.blit(self.background, self.background_rect) 
        self.all_bubbles.draw(self.screen)
        self.all_maus.draw(self.screen)    
        self.render = self.score.render(str(Settings.score), True, self.color)                
        pygame.display.flip()

    def updates(self):
        self.bubble.update()
        self.maus.update()



    def run(self):
        while not self.done:                
            self.clock.tick(Settings.fps)           
            for event in pygame.event.get():    
                if event.type == pygame.QUIT:   
                    self.done = True 
                elif event.type == pygame.KEYUP:          
                    if event.key == pygame.K_ESCAPE:
                        self.done = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass

            self.updates()
            self.show()
                      


if __name__ == '__main__':      
               
    game = Game()
    game.run()
    pygame.quit()