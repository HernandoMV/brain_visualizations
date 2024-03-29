
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image

# add the striatum limits
z_limits = [135, 307]
y_limits = [98, 271]

# file to process
# file_path = '/home/hernandom/data/Microscopy_Data/Optostimulation/D1andD2_Arch_histology-fibers_analysis/implant_coordinates.txt'
# file_path = '/home/hernandom/data/Microscopy_Data/Optostimulation/Dopamine_Optostimulation_histology_fibers_analysis/implant_coordinates.txt'
# file_path = '/home/hernandom/data/Microscopy_Data/Francesca_fiber_histology/implant_coordinates.txt'
# file_path = '/mnt/c/Users/herny/Desktop/SWC/Data/Microscopy_Data/Optostimulation/Dopamine_Optostimulation_histology_fibers_analysis/implant_coordinates.txt'
file_path = '/home/hernandom/data/Microscopy_Data/Francesca_fiber_histology/Reward-responses/implant_coordinates.txt'

# select number of slices to show, rows and cols
n_images = 12
rows = 4
cols = 3

# select the identifier to separate mice
# id_1 = 'D1'
# id_2 = 'D2'
id_1 = 'tStr'
# id_2 = 'Nac'
id_2 = 'SNL'

# select colors
# for D1 and D2 Arch
# color_1 = '#87CEEB'
# color_2 = '#056D6A'

# # photometry and DA stimulation
color_1 = '#002F3A' #tstr
color_2 = '#E95F32'

color_other = 'red'

# plot with a different marker the flat fibers and the tapered fibers
ff_marker = '_'
tf_marker = '|'


# atlas files paths
# atlas_path = '/mnt/c/Users/herny/Desktop/SWC/Data/Anatomy/ARA_25_micron_mhd/template_reversed.tif'
# atlas_path = '/mnt/c/Users/herny/Desktop/SWC/Data/Anatomy/AllanBrainAtlas_Images/AUDp_projections/Composite_with_atlas_RGB_green.tif'
# cp_image_path = '/mnt/c/Users/herny/Desktop/SWC/Data/Anatomy/AllanBrainAtlas_Images/Striatum_side_flat_with_AUD1proj_RGB_all.tif'
atlas_path = '/home/hernandom/data/Anatomy/AllanBrainAtlas_Images/AUDp_projections/Composite_with_atlas_RGB_green.tif'
cp_image_path = '/home/hernandom/data/Anatomy/AllanBrainAtlas_Images/Striatum_side_flat_with_AUD1proj_RGB_all_grey.tif'

fp = Path(file_path)
parent = fp.parent

# read the file of points
coords = pd.read_csv(file_path, header=0)
X = coords.x
Y = coords.y
Z = coords.z
Animal_Name = coords.Mouse_name

# select only the fibers used in the analysis
# CAREFUL HERE WITH WHERE IS LEFT AND WHERE IS RIGHT!!
# animals that are not included have a # in front of their name
animal_mask = [not an.startswith('#') for an in Animal_Name]
X = np.array(list(X[animal_mask])).astype(float)
Y = np.array(list(Y[animal_mask])).astype(float)
Z = np.array(list(Z[animal_mask])).astype(float)
Animal_Name = np.array(list(Animal_Name[animal_mask]))

# read atlas get slice numbers
atlas = Image.open(atlas_path)
h,w,_ = np.shape(atlas)
# decide on the number of images
step = int(np.floor((z_limits[1] - z_limits[0]) / n_images))
sl_list = list(range(z_limits[0], z_limits[1], step))
sl_list = sl_list[-n_images:]
# hack
# extreme tail focused:
# sl_list = [150, 200, 240,
#            265, 270, 275,
#            280, 285, 290,
#            295, 300, 305]

sl_list = [150, 175, 200,
           225, 235, 245,
           255, 265, 275,
           285, 295, 305]

# better coverage of NAc:
# sl_list = [160, 175, 190,
#            205, 235, 245,
#            255, 265, 275,
#            285, 295, 305]

# Mirror all to the right hemisphere
atlas_mid_point = w/2
for i in range(len(Z)):
    if Z[i] < atlas_mid_point:
        dist_to_center = atlas_mid_point - Z[i]
        Z[i] = atlas_mid_point + dist_to_center

# separate animals
mask_1 = [x.startswith(id_1) for x in Animal_Name]
mask_2 = [x.startswith(id_2) for x in Animal_Name]
mask_other = np.logical_and([not e for e in mask_1],
                            [not e for e in mask_2])

ff_mask = [x.endswith('_flat') for x in Animal_Name]
tf_mask = [not x for x in ff_mask]

# make the plot
fig, ax = plt.subplots(1, 1, figsize=[10,10])
# show striatum outline
str_im = Image.open(cp_image_path)
ax.imshow(str_im)
# show where slices are taken from
ax.vlines(sl_list, y_limits[0], y_limits[1],
          linestyles='dotted', color='grey', alpha=.3)
# plot points
for i in range(len(X)):
    if mask_1[i]:
        col = color_1
    if mask_2[i]:
        col = color_2
    if mask_other[i]:
        color_other
    if ff_mask[i]:
        mt = ff_marker
    if tf_mask[i]:
        mt = tf_marker
    ax.plot(X[i], Y[i], mt, color=col,
            alpha=.9, markersize=12, markeredgewidth=6)
# ax.plot(X[mask_2], Y[mask_2], 'x', color=color_2,
#         alpha=.8, markersize=10, markeredgewidth=4)
# ax.plot(X[mask_other], Y[mask_other], 'x', color=color_other,
#         alpha=.8, markersize=10, markeredgewidth=4)
# add limits of striatum
ax.set_ylim(bottom=y_limits[0], top=y_limits[1])
ax.set_xlim(left=z_limits[0], right=z_limits[1])
ax.set_aspect('equal', 'box')
ax.invert_yaxis()
# convert to mm
a=ax.get_xticks().tolist()
a= [25 * a[i] / 1000 for i in range(len(a))]
ax.set_xticklabels(a, fontsize=18)
a=ax.get_yticks().tolist()
a= [25 * a[i] / 1000 for i in range(len(a))]
ax.set_yticklabels(a, fontsize=18)
ax.set_xlabel('ARA A-P axis (mm)', fontsize=22)
ax.set_ylabel('ARA D-V axis (mm)', fontsize=22)

# Hide the right and top spines
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
plt.savefig(parent / 'sideview_plot.pdf',
            transparent=True, bbox_inches='tight')
# plt.show(fig)


# plot the fibers in the slices
fig2, axs = plt.subplots(rows, cols, figsize=[cols * w/50, rows * h/50])
axs = axs.ravel()
for c,i in enumerate(sl_list):
    atlas.seek(i)
    axs[c].imshow(atlas)#, cmap='gray_r')
    axs[c].axis('off')
# fig2.subplots_adjust(wspace=0, hspace=0)
fig2.tight_layout()

# plot the fibers
for c,x in enumerate(X):
    # find the index of the slice that this point is closest to
    templist = [np.abs(b - x) for b in sl_list]
    idx = np.argmin(templist)
    if mask_1[c]:
        col = color_1
    if mask_2[c]:
        col = color_2
    if mask_other[c]:
        col = color_other
    if ff_mask[c]:
        mt = ff_marker
    if tf_mask[c]:
        mt = tf_marker
    axs[idx].plot(Z[c], Y[c],
                  marker=mt, color=col, alpha=.8,
                  markersize=15, markeredgewidth=5)
plt.savefig(parent / 'slice_comp_plot.pdf',
            transparent=True, bbox_inches='tight')
# plt.show(fig2)
