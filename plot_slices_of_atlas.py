import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image

# file to process
atlas_path = '/mnt/c/Users/herny/Desktop/SWC/Data/Anatomy/AllanBrainAtlas_Images/AUDp_projections/Composite_double_with_atlas_outline.tif'
fp = Path(atlas_path)
parent = fp.parent

# select number of slices to show, rows and cols
n_images = 6
rows = 3
cols = 2

# add the striatum limits
z_limits = [135, 307]
y_limits = [98, 271]

# read atlas get slice numbers
atlas = Image.open(atlas_path)
h,w,_ = np.shape(atlas)
# decide on the number of images
step = int(np.floor((z_limits[1] - z_limits[0]) / n_images))
sl_list = list(range(z_limits[0], z_limits[1], step))
sl_list = sl_list[-n_images:]

sl_list = [245,
           255, 265, 275,
           285, 295]


# plot the fibers in the slices
fig2, axs = plt.subplots(rows, cols, figsize=[cols * w/50, rows * h/50])
axs = axs.ravel()
for c,i in enumerate(sl_list):
    atlas.seek(i)
    axs[c].imshow(atlas)#, cmap='gray_r')
    axs[c].axis('off')
# fig2.subplots_adjust(wspace=0, hspace=0)
fig2.tight_layout()

plt.savefig(parent / 'slice_comp_plot.pdf',
            transparent=True, bbox_inches='tight')