import time
import math
import pyvista as pv

heart_model = pv.read("Corazon.stl")

plotter = pv.Plotter()
plotter.add_mesh(heart_model, color='red')  

plotter.show(auto_close=False, interactive_update=True)

while True:
    try:
        with open("coords.txt", "r")as f:
            coords = f.read()
            if coords:
                x = float(coords.split(",")[0])
                y = float(coords.split(",")[1])
                plotter.camera.azimuth = x
                plotter.camera.elevation = y
                
    except FileNotFoundError:
        pass

    plotter.update()
    time.sleep(0.02)
