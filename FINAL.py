#!/usr/bin/env python3

#imports
import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityBodyYawspeed)
import pygame
import time
import math
#inits
pygame.init()
pygame.joystick.init()
#vars
ctrl = pygame.joystick.Joystick(0)
running=True
pos = pygame.Vector2(0,0)
posrel = pygame.Vector2(0,0)

#actual program
async def run():
    #definitions
    drone = System()#mavsdk_server_address=None, port=50051, sysid=245, compid=190
    #startup
    await drone.connect(system_address="udp://:14540")
    print("connected 1")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break
    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    #await drone.action.arm()


    #print("taking off")
    #await drone.action.set_takeoff_altitude(10.0)
    #await drone.action.takeoff()
    #time.sleep(10)
    #print("took off")
    
    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    
    
    #print("-- Starting offboard")
    #try:
    #    await drone.offboard.start()
    #except OffboardError as error:
    #    print(f"Starting offboard mode failed with error code: \
    #          {error._result.result}")
    #    print("-- Disarming")
     #   await drone.action.disarm()
     #   return
    
    
    
    #variables    
    alt = 0
    running = True
    rot = 0
    #main loops
    while running: 
        #x constraints
        #if pos.x < 0:
        #    pos.x += 0.05
        #elif pos.x > 0:
        #    pos.x -= 0.05
        if pos.x < -1:
            pos.x = -1
        if pos.x > 1:
            pos.x = 1
        #y constraints
        #if pos.y < 0:
        #    pos.y += 0.05
        #elif pos.y > 0:
        #    pos.y -= 0.05
        if pos.y < -1:
            pos.y = -1
        if pos.y > 1:
            pos.y = 1
        #climb constraints
        #if  alt < 0:
        #    alt += 0.2
        #elif alt > 0:
        #    alt -= 0.2
        if alt < -5:
            alt = -5
        if alt > 5:
            alt = 5
        #yaw constraints
        #if  rot < 0:
        #    rot += 0.5
        #elif rot > 0:
        #    rot -= 0.5
        if rot < -90:
            rot = -90
        if rot > 90:
            rot = 90
        
        #keybindings

        if ctrl.get_button(0) == 1:
            print("X")
            #pygame.quit()
            #exit()
        if ctrl.get_button(1) == 1:
            #print("A")
            alt += 0.5
        elif ctrl.get_button(2) == 1:
            #print("B")
            alt -= 0.5
        else:
            alt = 0
        if ctrl.get_button(3) == 1:
            print("Y")
        if ctrl.get_button(4) == 1:
            #print("L")
            rot -= 3
        elif ctrl.get_button(5) == 1:
            #print("R")
            rot += 3 
        else:
            rot = 0
        if ctrl.get_button(8) == 1:
            print("SELECT")
            #await drone.action.land()
            #time.sleep(4)
            #try:
            #    await drone.offboard.stop()
            #except OffboardError as error:
            #    print(f"Stopping offboard mode failed with error code: {error._result.result}")
            #    return
            #await drone.action.land()
            #time.sleep(4)

        if ctrl.get_button(9) == 1:
            print("START1")
            #await asyncio.sleep(3)
            #await drone.action.arm()
            #await drone.action.set_takeoff_altitude(10.0)
            #await drone.action.takeoff()
            #time.sleep(3)
            #print("-- Starting offboard")
            #await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0, 0.0))
            #try:
            #    await drone.offboard.start()
            #except OffboardError as error:
            #    print(f"Starting offboard mode failed with error code: {error._result.result}")
            #    print("-- Disarming")
            #    #await drone.action.disarm()
            #    await asyncio.sleep(3)
            #    return
        #AXES
        if round(ctrl.get_axis(1))==-1:
            pos.y -= 0.1
            #print("forward") 
        if round(ctrl.get_axis(1))==1:
            pos.y += 0.1 
            #print("back")
        if round(ctrl.get_axis(1))==0:
            pos.y = 0
        if round(ctrl.get_axis(0))==-1:
            pos.x += 0.1
            #print("left") 
        if round(ctrl.get_axis(0))==1:
            pos.x -= 0.1
            #print("right") 
        if round(ctrl.get_axis(0))==0:
            pos.x = 0
        #pos.y = ctrl.get_axis(0)
        #pos.x = ctrl.get_axis(1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #pos.y += (math.cos(rot)*posrel.y)+(math.cos(rot+90)*posrel.x)
        #pos.x += (math.sin(rot+90)*posrel.x)+(math.sin(rot)*posrel.y)
        
        #diagnostics

        #print(drone.telemetry.altitude())
        #async for flight_mode in drone.telemetry.flight_mode():
        #        print(f"Flight mode: {flight_mode}")
        
        #await drone.offboard.set_position_ned(PositionNedYaw(pos.y,-pos.x, -alt, rot))
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(pos.y, pos.x, -alt, rot))
        time.sleep(0.01)
if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
