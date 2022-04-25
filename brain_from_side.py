"""
    Print the brain from the side
"""
from brainrender import Scene
from brainrender import settings

settings.SHOW_AXES = False
settings.WHOLE_SCREEN = False

from rich import print
from myterial import orange
from pathlib import Path

top_camera = {
    'pos': (1814, -32863, -5453),
    'viewup': (-1, 0, 0),
    'clippingRange': (27457, 49150),
    'focalPoint': (6767, 4440, -5946),
    'distance': 37634,
}

plane_center = [8655.15806343, 4271.67187907, 5632.09744594]

print(f"[{orange}]Running\: {Path(__file__).name}")

# Plot all together:
scene = Scene(inset=False, title="")
region = scene.add_brain_region("CP", alpha=0.2)
scene.content
scene.render(camera=top_camera, zoom=1.2, interactive=True)
plane = scene.atlas.get_plane(pos=plane_center, norm=(-1, 0, 0))
scene.slice(plane)
# scene.screenshot(name='back_view_all.png')
scene.close()
