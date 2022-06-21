run("Close All");


// open images
path_to_folder = "/C:/Users/herny/Desktop/SWC/Data/Microscopy_Data/Histology_of_tail_lesions/Chronic_lesions/Data_for_figure/";
atlas_name = "Atlas_dimmed_inverted.tif";
perc_name = "merged_percentages.tif";
outline_name = "Outline_Gaussian_inCaudoputamen_3D.tif";

open(path_to_folder + atlas_name);
open(path_to_folder + perc_name);
run("Cyan");
open(path_to_folder + outline_name);
run("Magenta");

//define n of slices
cols = 3;
rows = 2;

sl_list = newArray(265, 270, 275, 280, 285, 290);

for (k = 0; k < sl_list.length; k++) {
	i = sl_list[k];
	selectWindow(atlas_name);
	setSlice(i);
	selectWindow(perc_name);
	setSlice(i);
	selectWindow(outline_name);
	setSlice(i);
	// overlay
	selectWindow(atlas_name);
	run("Add Image...", "image=" + perc_name + " x=0 y=0 opacity=100 zero");
	selectWindow(atlas_name);
	run("Add Image...", "image=" + outline_name + " x=0 y=0 opacity=100 zero");
	// duplicate image
	run("Duplicate...", "title=" + "slice-" + i);
}
//close and make stack
close(atlas_name);
close(perc_name);
close(outline_name);

run("Images to Stack", "name=Stack title=slice use");
selectWindow("Stack");
//crop in half
width = getWidth();
height = getHeight();
makeRectangle(width/2, 0, width/2, height);
run("Crop");
run("Flatten", "stack");

//make montage
run("Make Montage...", "columns=" + cols + " rows=" + rows + " scale=1 use");


