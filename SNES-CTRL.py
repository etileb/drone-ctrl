# Example file showing a basic pygame "game loop"
import pygame
size=[256,256]
# pygame setup
pygame.init()
pygame.joystick.init()
ctrl = pygame.joystick.Joystick(0)
screen = pygame.display.set_mode((256,256), pygame.RESIZABLE)
pygame.display.set_caption("SNES")
clock = pygame.time.Clock()
running = True
pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
dt = 0
while running:
    if ctrl.get_button(0) == 1:
        print("X")
    if ctrl.get_button(1) == 1:
        print("A")
    if ctrl.get_button(2) == 1:
        print("B")
    if ctrl.get_button(3) == 1:
        print("Y")
    if ctrl.get_button(4) == 1:
        print("L")
    if ctrl.get_button(5) == 1:
        print("R")
    if ctrl.get_button(6) == 1:
        print("6")
    if ctrl.get_button(7) == 1:
        print("7")
    if ctrl.get_button(8) == 1:
        print("SELECT")
    if ctrl.get_button(9) == 1:
        print("START")
    print()
    #if ctrl.get_button(10) == 1:
    #    print("10")
    #if ctrl.get_button(11) == 1:
    #    print("11")
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    if round(ctrl.get_axis(1))==-1:
        pos.y -= 200 * dt
    if round(ctrl.get_axis(1))==1:
        pos.y += 200 * dt
    if round(ctrl.get_axis(1))==0:
        pos.y = screen.get_height() / 2
    if round(ctrl.get_axis(0))==-1:
        pos.x -= 200 * dt
    if round(ctrl.get_axis(0))==1:
        pos.x += 200 * dt
    if round(ctrl.get_axis(0))==0:
        pos.x = screen.get_width() / 2
    
    pygame.draw.circle(screen, "red", pos, 20)


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limits FPS to 60

pygame.quit()