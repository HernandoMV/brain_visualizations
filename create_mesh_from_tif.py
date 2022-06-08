from support_file import extract_mesh_from_mask
from PIL import Image
import numpy as np
from vedo import write, Mesh

# read tif as np.array
orig_tif = '/home/hernandom/data/Anatomy/AllanBrainAtlas_Images/Vis_Aud_merge/AUD_thresholded_gaussian_25umpx-Caudoputamen.tif'
output = '/home/hernandom/data/Anatomy/AllanBrainAtlas_Images/Vis_Aud_merge/AUD_thresholded_gaussian_25umpx-Caudoputamen.obj'
dataset = Image.open(orig_tif)
h,w = np.shape(dataset)
tiffarray = np.zeros((h,w,dataset.n_frames))
for i in range(dataset.n_frames):
   dataset.seek(i)
   tiffarray[:,:,i] = np.array(dataset)

expim = tiffarray.astype(np.double)
print(expim.shape)
# extract mesh
mesh = extract_mesh_from_mask(volume=expim, obj_filepath=None, extract_largest=True)
# convert to microns
mesh_scaled = Mesh(mesh.points() * 25)
mesh_scaled.smooth()
# write to file
write(mesh_scaled, str(output))