from bg_atlasapi import BrainGlobeAtlas
import imio

bg_atlas = BrainGlobeAtlas("allen_mouse_25um")
# find number with print(bg_atlas.hierarchy)
stack = bg_atlas.get_structure_mask(477) 
stack = stack.astype(bool)
imio.to_tiff(stack, "/mnt/c/Users/herny/Desktop/striatum.tiff")