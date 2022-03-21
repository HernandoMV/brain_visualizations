"""
    Print tappered fiber tips from optoinhibition
"""
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

file_path = '/home/hernandom/fastdata/brainglobe-playground/implant_coordinates.txt'

fp = Path(file_path)

parent = fp.parent

print(parent)

top_camera = {
    'pos': (1814, -32863, -5453),
    'viewup': (-1, 0, 0),
    'clippingRange': (27457, 49150),
    'focalPoint': (6767, 4440, -5946),
    'distance': 37634,
}


print(f"[{orange}]Running\: {Path(__file__).name}")

scene = Scene(inset=False, title="fiber tips", screenshots_folder=parent)

region = scene.add_brain_region(
    "CP",
    alpha=0.2,
)

# read the file of points and correct resolution
coords = pd.read_csv(file_path, header=0)
X = 25 * coords.x
Y = 25 * coords.y
Z = 25 * coords.z

pts = np.array([[x, y, z] for x, y, z in zip(X, Y, Z)])
# print(pts)

# Add to scene
scene.add(Points(pts, name="fiber_tips", colors="red", radius=150, alpha=.1))

scene.content
# scene.slice('frontal')
scene.render(camera=top_camera, zoom=1.2, interactive=False)

scene.screenshot(name='top_view_all.png')

scene.close()
