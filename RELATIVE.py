#!/usr/bin/env python3


import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityBodyYawspeed)
import pygame
import time
import math
pygame.init()
pygame.joystick.init()
ctrl = pygame.joystick.Joystick(0)
running=True
pos = pygame.Vector2(0,0)
posrel = pygame.Vector2(0,0)

async def run():
    """ Does Offboard control using velocity body coordinates. """

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

    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
              {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    #print("-- Turn clock-wise and climb")
    #await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, -1.0, 60.0))
    #await asyncio.sleep(5)

    #print("-- Turn back anti-clockwise")
    #await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, -60.0))
    #await asyncio.sleep(5)

    #print("-- Wait for a bit")
    #await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    #await asyncio.sleep(2)

    #print("-- Fly a circle")
    #await drone.offboard.set_velocity_body(VelocityBodyYawspeed(5.0, 0.0, 0.0, 30.0))
    #await asyncio.sleep(15)

    #print("-- Wait for a bit")
    #await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    #await asyncio.sleep(5)

    #print("-- Fly a circle sideways")
    #await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, -5.0, 0.0, 30.0))
    #await asyncio.sleep(15)

    #print("-- Wait for a bit")
    #await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    #await asyncio.sleep(8)

    #print("-- Stopping offboard")
    #try:
    #    await drone.offboard.stop()
    #except OffboardError as error:
    #    print(f"Stopping offboard mode failed with error code: \
    #          {error._result.result}")

    alt = 0
    airborne = True
    counter = 1
    running = True
    rot = 0
    while running: 
        #x constraints
        if pos.x < 0:
            pos.x += 0.05
        elif pos.x > 0:
            pos.x -= 0.05
        if pos.x < -1:
            pos.x = -1
        if pos.x > 1:
            pos.x = 1
        #y constraints
        if pos.y < 0:
            pos.y += 0.05
        elif pos.y > 0:
            pos.y -= 0.05
        if pos.y < -1:
            pos.y = -1
        if pos.y > 1:
            pos.y = 1
        #climb constraints
        if  alt < 0:
            alt += 0.2
        elif alt > 0:
            alt -= 0.2
        if alt < -5:
            alt = -5
        if alt > 5:
            alt = 5
        #yaw constraints
        if  rot < 0:
            rot += 0.5
        elif rot > 0:
            rot -= 0.5
        if rot < -60:
            rot = -60
        if rot > 60:
            rot = 60

        #pos.x = 0

        #pos.y = 0
        #rot = 0

        if ctrl.get_button(0) == 1:
            print("X")
            pygame.quit()
            exit()
        if ctrl.get_button(1) == 1:
            #print("A")
            alt += 0.5
        if ctrl.get_button(2) == 1:
            #print("B")
            alt -= 0.5
        if ctrl.get_button(3) == 1:
            print("Y")
        if ctrl.get_button(4) == 1:
            #print("L")
            rot -= 1.5
        if ctrl.get_button(5) == 1:
            #print("R")
            rot += 1.5 
        if ctrl.get_button(8) == 1:
            print("SELECT")
            
        if ctrl.get_button(9) == 1:
            #print("START")
            if airborne == True:
                await drone.action.land()
                await asyncio.sleep(3)
                try:
                    await drone.offboard.stop()
                except OffboardError as error:
                    print(f"Stopping offboard mode failed with error code: {error._result.result}")
                airborne = False
            else:
                await drone.action.arm()
                await drone.action.takeoff()
                print("-- Starting offboard")
                try:
                    await drone.offboard.start()
                except OffboardError as error:
                    print(f"Starting offboard mode failed with error code: {error._result.result}")
                    print("-- Disarming")
                    await drone.action.disarm()
                    return
                airborne = True
                await asyncio.sleep(3)
        #AXES
        if round(ctrl.get_axis(1))==-1:
            pos.y += 0.1
            #print("forward") 
        if round(ctrl.get_axis(1))==1:
            pos.y -= 0.1 
            #print("back")
        #if round(ctrl.get_axis(1))==0:
        #    pos.y = 0
        if round(ctrl.get_axis(0))==-1:
            pos.x += 0.1
            #print("left") 
        if round(ctrl.get_axis(0))==1:
            pos.x -= 0.1
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
        
        print(round(pos,2),round(alt,2))
        
        #await drone.offboard.set_position_ned(PositionNedYaw(pos.y,-pos.x, -alt, rot))
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(pos.y, pos.x, -alt, rot))
        time.sleep(0.01)
if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
