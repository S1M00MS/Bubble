import pygame, os, random, time
pygame.init()

class Settings(object):
    width = 600
    height = 400
    fps = 60       
    title = "Bubble" 
    file_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "imagesbubble")
    bordersize = 10
    score = 0
    scorefont = pygame.font.SysFont("Arial", 20, True, False)
    color = (0, 0, 0)
    pause = False
    end = False

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)



class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 5
        self.image_original = pygame.image.load(os.path.join(Settings.images_path, "bubble.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image_original, (self.radius * 2,self.radius * 2))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.r = random.randrange(1,5)
        self.starttime = 0


    def update(self):
        self.starttime += 1
        if self.starttime == 60:
            self.starttime = 0
            self.radius += self.r
            c = self.rect.center
            self.rect.width = self.radius * 2
            self.rect.height = self.radius * 2
            self.image = pygame.transform.scale(self.image_original, (self.rect.width, self.rect.height))
            self.rect.center = c
            
        if pygame.mouse.get_pressed()[0]:
            if pygame.mouse.get_pos()[0] >= self.rect.left and pygame.mouse.get_pos()[0] <= self.rect.right and pygame.mouse.get_pos()[1] >= self.rect.top and pygame.mouse.get_pos()[1] <= self.rect.bottom:
                self.kill()
                Settings.score += self.radius
    
class Spawnbubble(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 15
        self.image_original = pygame.image.load(os.path.join(Settings.images_path, "bubble.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image_original, (self.radius * 2,self.radius * 2))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(Settings.bordersize, Settings.width - Settings.bordersize)
        self.rect.centery = random.randrange(Settings.bordersize, Settings.height - Settings.bordersize)
        

    def update(self):
        self.rect.centerx = random.randrange(Settings.bordersize, Settings.width - Settings.bordersize)
        self.rect.centery = random.randrange(Settings.bordersize, Settings.height - Settings.bordersize)
      
            

class Maus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "maus.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.left = pygame.mouse.get_pos() [0]
        self.rect.top = pygame.mouse.get_pos() [1]

class Pause():
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.get_dim())
        self.p = pygame.image.load(os.path.join(Settings.images_path, "background2.png"))
        self.p = pygame.transform.scale(self.p, (Settings.width, Settings.height))
        self.p_rect = self.p.get_rect()
        self.p.set_alpha(200)


    def show(self):
        self.screen.blit(self.p, self.p_rect)
        pygame.display.flip()
        Settings.pause = True


class Endscreen():
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.get_dim())
        self.e = pygame.image.load(os.path.join(Settings.images_path, "background2.png")).convert()
        self.e = pygame.transform.scale(self.e, (Settings.width, Settings.height))
        self.e_rect = self.e.get_rect()
        self.scorefont  = pygame.font.SysFont("Arial", 60, True, False)
        

    def show(self):
        self.screen.blit(self.e, self.e_rect) 
        self.render = self.scorefont.render(str(Settings.score), True, Settings.color)
        self.screen.blit(self.render, ((Settings.width // 2) - 40, (Settings.height // 2) - 30))
        pygame.display.flip()
        Settings.end = True


class save_score():
    def __init__(self):
        self.datei_name = ('Score.txt')
        self.text = Settings.score

    def ausgabe(self):
        file = open(self.datei_name,'a')
        file.write(self.text+ '\n')

class Game():
    def __init__(self):
        #settings
        self.dropcounter = 0
        self.clock = pygame.time.Clock()
        self.done = False
        self.screen = pygame.display.set_mode(Settings.get_dim())
        self.endscreen = Endscreen()
        self.pause = Pause()
        self.bool = True
        pygame.display.set_caption(Settings.title)
        #Background erstellen
        self.background = pygame.image.load(os.path.join(Settings.images_path, "background2.png")).convert()
        self.background = pygame.transform.scale(self.background, (Settings.width, Settings.height))
        self.background_rect = self.background.get_rect()

        #sprites
        self.all_bubbles = pygame.sprite.Group()
        self.bubble = Bubble(random.randrange(Settings.bordersize, Settings.width - Settings.bordersize), random.randrange(Settings.bordersize, Settings.height - Settings.bordersize))
        self.all_bubbles.add(self.bubble)

        self.spawnbubble = Spawnbubble()

        self.all_maus = pygame.sprite.Group()
        self.maus = Maus()
        self.all_maus.add(self.maus)


        pygame.mouse.set_visible(False)

    def spawn(self):
        self.bubble = Bubble(self.spawnbubble.rect.centerx, self.spawnbubble.rect.centery)
        self.all_bubbles.add(self.bubble)
        self.dropcounter = 0
    
    def show(self):
        self.screen.blit(self.background, self.background_rect) 
        self.all_bubbles.draw(self.screen)
        self.all_maus.draw(self.screen)    
        self.render = Settings.scorefont.render(str(Settings.score), True, Settings.color)
        self.screen.blit(self.render, (Settings.bordersize, Settings.bordersize))               
        pygame.display.flip()

    def updates(self):
        self.all_bubbles.update()
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
                    if event.key == pygame.K_p:
                        if Settings.pause == False:
                            self.pause.show()
                        else:
                            Settings.pause = False
        
            if Settings.pause == False and Settings.end == False:

                #spawn collision
                if self.dropcounter >= 60:
                    self.spawnbubble.update()
                    while self.bool == True:
                        for self.bubble in self.all_bubbles:
                            if pygame.sprite.collide_circle(self.spawnbubble, self.bubble):
                                self.spawnbubble.update()
                            else:
                                self.bool = False
                    self.spawn()
                else:
                    self.dropcounter += 1


                self.updates()
                self.show()

                #collision
                for b1 in self.all_bubbles:
                    for b2 in self.all_bubbles:
                        if b1 != b2:
                            collision = pygame.sprite.collide_circle(b1, b2)
                            if bool(collision):
                                self.endscreen.show()
                                
                      


if __name__ == '__main__':      
               
    game = Game()
    game.run()
    pygame.quit()