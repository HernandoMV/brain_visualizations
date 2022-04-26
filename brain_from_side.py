"""
    Print the brain from the side
"""
from brainrender import Scene
from brainrender import settings
from brainrender.actors import Cylinder

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
region = scene.add_brain_region("CP", alpha=0.2, color="green")
scene.content

# Slice actors with frontal plane
# scene.slice("sagital", actors=[th])

# Slice with a custom plane
# plane = scene.atlas.get_plane(pos=mos.centerOfMass(), norm=(1, 1, 0))
scene.slice('sagittal')#, actors=[region])


# plane = scene.atlas.get_plane(pos=plane_center, norm=(0, 0, -1))
# scene.slice(plane)

print(region.mesh.bounds()[0])
print(region.points().mean(axis=0))

# create and add a cylinder actor
cil_tail = Cylinder(
    pos=[7300, 3900, 2100],  # center the cylinder at the center of mass of th
    root=scene.root,  # the cylinder actor needs information about the root mesh
    color="red",
    alpha=1,
    radius=300
)

scene.add(cil_tail)


cil_nac = Cylinder(
    pos=[4700, 5200, 4000],  # center the cylinder at the center of mass of th
    root=scene.root,  # the cylinder actor needs information about the root mesh
    color="red",
    alpha=1,
    radius=300
)

scene.add(cil_nac)


scene.render(camera='sagittal', zoom=1.2, interactive=True)

# scene.screenshot(name='back_view_all.png')
scene.close()
