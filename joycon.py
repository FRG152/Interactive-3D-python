import pygame
import time

zoom = 1.000

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No hay ningún joystick conectado.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Usando el joystick: {joystick.get_name()}")

try:
    while True:
        pygame.event.pump()  
        events = pygame.event.get()

        x_axis = joystick.get_axis(0)  
        y_axis = joystick.get_axis(1)  

        for event in events:
            if event.dict.get("button") == 1:
                zoom += 0.001
            elif event.dict.get("button") == 3:
                zoom -= 0.001

        with open("coords.txt", "w") as f:
            f.write(f"{x_axis},{y_axis},{zoom:.3f}")
            
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nSaliendo...")
finally:
    pygame.quit()
