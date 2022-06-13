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
# file_path = '/home/hernandom/data/Microscopy_Data/Optostimulation/Dopamine_Optostimulation_histology_fibers_analysis/implant_coordinates.txt'
# file_path = '/home/hernandom/data/Microscopy_Data/Francesca_fiber_histology/implant_coordinates.txt'
# file_path = '/mnt/c/Users/herny/Desktop/SWC/Data/Microscopy_Data/Optostimulation/D1andD2_Arch_histology-fibers_analysis/implant_coordinates.txt'

# Mirror the image
mirror = True

# select the identifier to separate mice
id_1 = 'D1'
id_2 = 'D2'
# id_1 = 'tStr'
# id_2 = 'Nac'

# # select colors
# # for D1 and D2 Arch
color_1 = '#87CEEB'
color_2 = '#056D6A'

# # photometry and DA stimulation
# color_1 = '#002F3A' #tstr
# color_2 = '#E95F32'

fp = Path(file_path)
parent = fp.parent

top_half_camera = {
    'pos': (2561, -19083, -5807),
     'viewup': (-1, 0, 0),
     'clippingRange': (12258, 36810),
     'focalPoint': (6314, 4543, -2712),
     'distance': 24122,
}

top_camera = {
    'pos': (1814, -32863, -5453),
    'viewup': (-1, 0, 0),
    'clippingRange': (27457, 49150),
    'focalPoint': (6767, 4440, -5946),
    'distance': 37634,
}

back_camera = {
    'pos': (32023, -388, -5767),
    'viewup': (0, -1, 0),
    'clippingRange': (17887, 40832),
    'focalPoint': (6732, 4204, -5674),
    'distance': 25705,
}

zoom_camera = {
     'pos': (24178, 1210, -3760),
     'viewup': (0, -1, 0),
     'clippingRange': (9250, 33210),
     'focalPoint': (6633, 3937, -2468),
     'distance': 17803,
}

plane_center = [8655.15806343, 4271.67187907, 5632.09744594]
# own_mesh = '/home/hernandom/data/Anatomy/AllanBrainAtlas_Images/Vis_Aud_merge/AUD_thresholded_gaussian_25umpx-Caudoputamen.obj'

print(f"[{orange}]Running\: {Path(__file__).name}")

# read the file of points and correct resolution
coords = pd.read_csv(file_path, header=0)
X = 25 * coords.x
Y = 25 * coords.y
Z = 25 * coords.z
Animal_Name = coords.Mouse_name

# select only the fibers used in the analysis
# CAREFUL HERE WITH WHERE IS LEFT AND WHERE IS RIGHT!!
# animals that are not included have a # in front of their name
animal_mask = [not an.startswith('#') for an in Animal_Name]
X = np.array(list(X[animal_mask])).astype(float)
Y = np.array(list(Y[animal_mask])).astype(float)
Z = np.array(list(Z[animal_mask])).astype(float)
Animal_Name = np.array(list(Animal_Name[animal_mask]))

# Plot all together:

# top view
scene = Scene(inset=False, title="", screenshots_folder=parent)
region = scene.add_brain_region("CP",alpha=0.2, color='gray')
region2 = scene.add_brain_region("ACB",alpha=0.2, color='gray')
region3 = scene.add_brain_region("FS",alpha=0.2, color='gray')

# Mirror all to the right hemisphere
if mirror:
    atlas_mid_point = region.centerOfMass()[2]
    for i in range(len(Z)):
        if Z[i] > atlas_mid_point:
            dist_to_center = atlas_mid_point - Z[i]
            Z[i] = atlas_mid_point + dist_to_center

# import the custom mesh from AU1 TODO
# scene.add(own_mesh, color="tomato")
fname = ''
if mirror:
    fname = '_mirror'

pts = np.array([[x, y, z] for x, y, z in zip(X, Y, Z)])
for i in range(len(Animal_Name)):
    if Animal_Name[i].startswith(id_1):
        scene.add(Points(np.array([pts[i]]), name="fiber_tips", colors=color_1, radius=50, alpha=.8))
    if Animal_Name[i].startswith(id_2):
        scene.add(Points(np.array([pts[i]]), name="fiber_tips", colors=color_2, radius=50, alpha=.8))
# scene.add(Points(pts, name="fiber_tips", colors="#87CEEB", radius=50, alpha=.2))
scene.content
scene.render(camera=top_half_camera, zoom=1.2, interactive=False)
scene.screenshot(name='top_half_view_all' + fname + '.png')

scene.render(camera=top_camera, zoom=1.2, interactive=False)
scene.screenshot(name='top_view_all' + fname + '.png')

# back view
scene.render(camera=back_camera, zoom=1.2, interactive=False)
plane = scene.atlas.get_plane(pos=plane_center, norm=(-1, 0, 0))
scene.slice(plane)
scene.screenshot(name='back_view_all' + fname + '.png')

# zoom view
plane = scene.atlas.get_plane(pos=plane_center, norm=(-1, 0, 0))
scene.render(camera=zoom_camera, zoom=1.2, interactive=False)
scene.screenshot(name='zoom_view_all' + fname + '.png')

# close
scene.close()



# # Plot each mouse individually
# for an_name in np.unique(Animal_Name):
#     print(an_name)
#     # get points
#     an_idx = np.where(Animal_Name==an_name)[0]
#     an_pts = pts[an_idx]
#     # plot
#     scene = Scene(inset=False, title="", screenshots_folder=parent)
#     region = scene.add_brain_region("CP",alpha=0.2)
#     scene.add(Points(an_pts, name="fiber_tips", colors="red", radius=150, alpha=1))
#     scene.render(camera=top_camera, zoom=1.2, interactive=False)
#     scene.screenshot(name='top_view' + an_name + '.png')
#     scene.render(camera=back_camera, zoom=1.2, interactive=False)
#     plane = scene.atlas.get_plane(pos=plane_center, norm=(-1, 0, 0))
#     scene.slice(plane)
#     scene.screenshot(name='back_view_all' + an_name + '.png')
#     scene.close()
