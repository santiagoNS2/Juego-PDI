import pygame

pygame.init()

# Crear una ventana
window = pygame.display.set_mode((800, 300),x=0,y=0)

# Mantener la ventana abierta
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Salir de Pygame
pygame.quit()
