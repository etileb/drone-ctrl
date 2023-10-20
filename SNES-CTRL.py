import pygame
import time
import asyncio
from mavsdk import System
from pymavlink import mavutil
pygame.init()
pygame.joystick.init()
ctrl = pygame.joystick.Joystick(0)
#screen = pygame.display.set_mode((256,256), pygame.RESIZABLE)
#pygame.display.set_caption("SNES")
clock = pygame.time.Clock()
running = True
pos = pygame.Vector2(0,0)
rot = 0
dt = 0
conn = mavutil.mavlink_connection('udpin:localhost:14540')
conn.wait_heartbeat()
conn.mav.command_long_send(conn.target_system, conn.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,0,1,0,0,0,0,0,0)
print("Heartbeat from system (system %u component %u)" % (conn.target_system, conn.target_component))
#while ctrl.get_button(8) == 0:
#    print("start me")

#while 1==1:
#    print(ctrl.get_axis(0))
while running:
    

    if ctrl.get_button(0) == 1:
        print("X")
        running = False
    if ctrl.get_button(1) == 1:
        print("A")
    if ctrl.get_button(2) == 1:
       print("B")
    if ctrl.get_button(3) == 1:
        print("Y")
    if ctrl.get_button(4) == 1:
        print("L")
        rot -= 10
    if ctrl.get_button(5) == 1:
        print("R")
        rot += 10 
    if ctrl.get_button(8) == 1:
        print("SELECT")
        conn.mav.command_long_send(conn.target_system, conn.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,0,1,0,0,0,0,0,0)
    if ctrl.get_button(9) == 1:
        print("START")
        conn.mav.command_long_send(conn.target_system, conn.target_component, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,0,0,0,0,0,0,0,10)
        #conn.mav.command_long_send(conn.target_system, conn.target_component, mavutil.mavlink.MAV_CMD_NAV_LAND,0,0,2,0,0,0,0,0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    #if round(ctrl.get_axis(1))==-1:
        #pos.y -= 200 
    #if round(ctrl.get_axis(1))==1:
        #pos.y += 200 
    #if round(ctrl.get_axis(1))==0:
        #pos.y = 0
    #if round(ctrl.get_axis(0))==-1:
        #pos.x -= 200 
    #if round(ctrl.get_axis(0))==1:
        #pos.x += 200 
    #if round(ctrl.get_axis(0))==0:
        #pos.x = 0
     
    
    #pygame.draw.circle(screen, "red", pos, 20)


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    #pygame.display.flip()

    time.sleep(0.01)  # limits FPS to 60

pygame.quit()
exit()