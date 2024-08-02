import pygame, random

 



ANCHO = 800
ALTO = 600
BLACK = (0,0,0)
WHITE = (255, 255, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Aventura Espacial")
clock = pygame.time.Clock()

def show_menu():
    # Colores para el menú
    MENU_BG_COLOR = BLACK
    MENU_TEXT_COLOR = WHITE

    # Crear una fuente para el texto del menú
    font = pygame.font.SysFont(None, 55)
    
    # Mensaje de título
    title_text = font.render("Aventura Espacial", True, MENU_TEXT_COLOR)
    title_rect = title_text.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    
    # Mensaje de instrucciones
    instructions_text = font.render("Presiona una tecla para comenzar", True, MENU_TEXT_COLOR)
    instructions_rect = instructions_text.get_rect(center=(ANCHO // 2, ALTO // 2 + 10))

    waiting = True
    while waiting:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        # Dibujar el fondo del menú
        screen.fill(MENU_BG_COLOR)
        
        # Dibujar el título y las instrucciones
        screen.blit(title_text, title_rect)
        screen.blit(instructions_text, instructions_rect)

        # Actualizar la pantalla
        pygame.display.flip()

def new_game():
    global all_sprites, asteroides_list, balas_list, player
    
    all_sprites = pygame.sprite.Group()
    asteroides_list = pygame.sprite.Group()
    balas_list = pygame.sprite.Group()
    
    player = Player()
    all_sprites.add(player)
    
    for i in range(8):
        asteroide = Asteroide()
        all_sprites.add(asteroide)
        asteroides_list.add(asteroide)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("nave.png").convert()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensiona la imagen de la nave
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 2
        self.speed_x = 0
    def update(self):
            self.speed_x= 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                  self.speed_x = -5
            if keystate[pygame.K_RIGHT]:
                  self.speed_x = 5
            self.rect.x += self.speed_x            
            if self.rect.right > ANCHO:
                  self.rect.right = ANCHO
            if self.rect.left < 0:
                  self.rect.left = 0    

    def disparo(self):
          bala = Bala(self.rect.centerx, self.rect.top)
          all_sprites.add(bala)
          balas_list.add(bala)

class Asteroide(pygame.sprite.Sprite): 
      def __init__(self):
            super().__init__()
            self.image = pygame.image.load("asteroide.png").convert()
            self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensiona la imagen del asteroide
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1,10)
            self.speedx = random.randrange(-5, 5)

      def update(self):
            self.rect.y += self.speedy  
            self.rect.x += self.speedx
            if self.rect.top > ALTO + 10 or self.rect.left < -25 or self.rect.right > ANCHO + 25:
                  self.rect.x = random.randrange(ANCHO - self.rect.width)  
                  self.rect.y = random.randrange(-100, -40)
                  self.speedy = random.randrange(1, 10)   

class Bala(pygame.sprite.Sprite):
      def __init__(self, x, y):
            super().__init__()
            self.image =  pygame.image.load("bala.png")
            self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensiona la imagen de la bala
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.centerx = x
            self.speedy = -10

      def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                  self.kill()
                 
background = pygame.image.load("imagen_de_fondo.png").convert()                  
background = pygame.transform.scale(background, (ANCHO, ALTO))
               
                  

all_sprites = pygame.sprite.Group()
asteroides_list = pygame.sprite.Group()
balas_list = pygame.sprite.Group()
player = Player()
all_sprites.add(player)



for i in range(8):
      asteroide = Asteroide()
      all_sprites.add(asteroide)
      asteroides_list.add(asteroide)

show_menu()  # Mostrar el menú al inicio del juego
new_game() 
        
corriendo = True
while corriendo:
            # clock.tick(60)
             for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                    corriendo = False

                 elif event.type == pygame.KEYDOWN:
                       if event.key == pygame.K_SPACE:
                        player.disparo()
                             
             all_sprites.update()

             hits = pygame.sprite.groupcollide(asteroides_list, balas_list, True, True)
             for hit in hits:
                   asteroide = Asteroide()
                   all_sprites.add(asteroide)
                   asteroides_list.add(asteroide)

             hits = pygame.sprite.spritecollide(player, asteroides_list, True)
             if hits:
                  show_menu()  # Mostrar el menú después de una pérdida
                  new_game()   # Reiniciar el juego
                  continue  # Continuar con el siguiente ciclo del bucle     
        
             screen.blit(background, [0, 0])
             all_sprites.draw(screen)
             pygame.display.flip()

             clock.tick(60)

pygame.quit()

        
