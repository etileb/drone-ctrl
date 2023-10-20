#!/usr/bin/env python3

"""
Caveat when attempting to run the examples in non-gps environments:

`drone.offboard.stop()` will return a `COMMAND_DENIED` result because it
requires a mode switch to HOLD, something that is currently not supported in a
non-gps environment.
"""
import math
import asyncio
import time
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
import pygame
pygame.init()
pygame.joystick.init()
ctrl = pygame.joystick.Joystick(0)
running=True
pos = pygame.Vector2(0,0)
posrel = pygame.Vector2(0,0)
rot = 0
alt = 0
airborne = False
async def takeoff():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
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
    await drone.action.arm()

    print("takeoff")
    await drone.action.takeoff()

async def run():
    airborne = True
    counter = 1
    running = True
    print(""" Does Offboard control using position NED coordinates. """)
    drone = System()
    await drone.connect(system_address="udp://:14540")
    alt = 0
    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
        print('offboard active')
    except OffboardError as error:
        print("Starting offboard mode failed \
                with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return
        exit()
    rot = 0
    while running: 
        posrel.x = 0
        posrel.y = 0
        #rot = 0

        if ctrl.get_button(0) == 1:
            print("X")
            pygame.quit()
            exit()
        if ctrl.get_button(1) == 1:
            #print("A")
            alt += 0.02
        if ctrl.get_button(2) == 1:
            #print("B")
            alt -= 0.02
        if ctrl.get_button(3) == 1:
            print("Y")
        if ctrl.get_button(4) == 1:
            #print("L")
            rot -= 1
        if ctrl.get_button(5) == 1:
            #print("R")
            rot += 1 
        if ctrl.get_button(8) == 1:
            print("SELECT")
            
        if ctrl.get_button(9) == 1:
            #print("START")
            if airborne == True:
                await drone.action.land()
                airborne = False
            else:
                await drone.action.arm()
                await drone.action.takeoff()
                airborne = True
        #AXES
        if round(ctrl.get_axis(1))==-1:
            posrel.y += 0.01
            #print("forward") 
        if round(ctrl.get_axis(1))==1:
            posrel.y -= 0.01 
            #print("back")
        #if round(ctrl.get_axis(1))==0:
        #    pos.y = 0
        if round(ctrl.get_axis(0))==-1:
            posrel.x += 0.01
            #print("left") 
        if round(ctrl.get_axis(0))==1:
            posrel.x -= 0.01
            #print("right") 
        #if round(ctrl.get_axis(0))==0:
        #    pos.x = 0
        #pos.y = ctrl.get_axis(0)
        #pos.x = ctrl.get_axis(1)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pos.y += (math.cos(rot)*posrel.y)+(math.cos(rot+90)*posrel.x)
        pos.x += (math.sin(rot+90)*posrel.x)+(math.sin(rot)*posrel.y)
        
        print(posrel)
        
        await drone.offboard.set_position_ned(PositionNedYaw(pos.y,-pos.x, -alt, rot))
        time.sleep(0.01)
    #await asyncio.sleep(10)

    #print("-- Go 5m North, 0m East, -5m Down \
    #        within local coordinate system, turn to face East")
    #await drone.offboard.set_position_ned(
    #        PositionNedYaw(5.0, 0.0, -5.0, 90.0))
    #await asyncio.sleep(10)

    #print("-- Go 5m North, 10m East, -5m Down \
    #        within local coordinate system")
    #await drone.offboard.set_position_ned(
    #        PositionNedYaw(5.0, 10.0, -5.0, 90.0))
    #await asyncio.sleep(15)

    #print("-- Go 0m North, 10m East, 0m Down \
    #        within local coordinate system, turn to face South")
    #await drone.offboard.set_position_ned(
    #        PositionNedYaw(0.0, 10.0, 0.0, 180.0))
    #await asyncio.sleep(10)
async def land():
    drone = System()
    await drone.action.land()
    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed \
                with error code: {error._result.result}")    

if __name__ == "__main__":
    asyncio.run(takeoff())
    airborne = True
    # Run the asyncio loop
    asyncio.run(run())