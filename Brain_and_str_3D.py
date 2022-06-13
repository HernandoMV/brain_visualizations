"""
    Print tappered fiber tips from optoinhibition
"""
from dis import dis
# from math import dist
from brainrender import Scene
from brainrender import settings
import numpy as np
import pandas as pd

from brainrender.actors import Points

settings.SHOW_AXES = False
settings.WHOLE_SCREEN = False

from rich import print
from myterial import orange
from pathlib import Path

file_path = '/home/hernandom/data/Microscopy_Data/Optostimulation/D1andD2_Arch_histology-fibers_analysis/implant_coordinates.txt'
# file_path = '/home/hernandom/fastdata/DAopto_histology/implant_coordinates.txt'
# file_path = '/home/hernandom/fastdata/Francesca_fiber_histology/implant_coordinates.txt'

fp = Path(file_path)
parent = fp.parent

top_camera = {
    'pos': (1814, -32863, -5453),
    'viewup': (-1, 0, 0),
    'clippingRange': (27457, 49150),
    'focalPoint': (6767, 4440, -5946),
    'distance': 37634,
}


# top view
scene = Scene(inset=False, title="", screenshots_folder=parent)
region = scene.add_brain_region("CP",alpha=0.2, color='gray')
region2 = scene.add_brain_region("ACB",alpha=0.2, color='gray')
region3 = scene.add_brain_region("FS",alpha=0.2, color='gray')
scene.content
scene.render(camera=top_camera, zoom=1.2, interactive=False)
scene.screenshot(name='brain_and_str.png')
# close
scene.close()

