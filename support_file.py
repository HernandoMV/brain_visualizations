try:
    from vedo import Mesh, write, load, show, Volume
    from vedo.applications import Browser
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Mesh generation with these utils requires vedo\n"
        + '   please install with "pip install vedo -U"'
    )

try:
    import mcubes
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Mesh generation with these utils requires PyMCubes\n"
        + '   please install with "pip install PyMCubes -U"'
    )

from loguru import logger
import numpy as np
from pathlib import Path
import scipy

# ---------------------------------------------------------------------------- #
#                                 MESH CREATION                                #
# ---------------------------------------------------------------------------- #


def extract_mesh_from_mask(
    volume,
    obj_filepath=None,
    threshold=0.5,
    smooth: bool = False,
    mcubes_smooth=False,
    closing_n_iters=8,
    decimate_fraction: float = 0.6,  # keep 60% of original fertices
    use_marching_cubes=False,
    extract_largest=False,
):
    """
    Returns a vedo mesh actor with just the outer surface of a
    binary mask volume. It's faster though less accurate than
    extract_mesh_from_mask


    Parameters
    ----------
    obj_filepath: str or Path object
        path to where the .obj mesh file will be saved
    volume: 3d np.ndarray
    threshold: float
        min value to threshold the volume for isosurface extraction
    smooth: bool
        if True the surface mesh is smoothed
    use_marching_cubes: bool:
        if true PyMCubes is used to extract the volume's surface
        it's slower and less accurate than vedo though.
    mcubes_smooth: bool,
        if True mcubes.smooth is used before applying marching cubes
    closing_n_iters: int
        number of iterations of closing morphological operation.
        set to None to avoid applying morphological operations
    decimate_fraction: float  in range [0, 1].
        What fraction of the original number of vertices is to be kept. E.g. .5 means that
        50% of the vertices are kept, the others are removed
    tol: float
        parameter for decimation, larger values correspond to more aggressive decimation.
        E.g. 0.02 -> points that are closer than 2% of the size of the meshe's bounding box are
        identified and removed (only one is kep)
    extract_largest: bool
        If True only the largest region are extracted. It can cause issues for
        bilateral regions as only one will remain

    """
    # check savepath argument
    if obj_filepath is not None:
        if isinstance(obj_filepath, str):
            obj_filepath = Path(obj_filepath)

        if not obj_filepath.parents[0].exists():
            raise FileExistsError(
                "The folder where the .obj file is to be saved doesn't exist"
                + f"\n      {str(obj_filepath)}"
            )

    # Check volume argument
    if np.min(volume) > 0 or np.max(volume) < 1:
        raise ValueError(
            "Argument volume should be a binary mask with only 0s and 1s when passing a np.ndarray"
        )

    # Apply morphological transformations
    if closing_n_iters is not None:
        volume = scipy.ndimage.morphology.binary_fill_holes(volume)
        volume = scipy.ndimage.morphology.binary_closing(
            volume, iterations=closing_n_iters
        )

    if not use_marching_cubes:
        # Use faster algorithm
        volume = Volume(volume)
        mesh = volume.clone().isosurface(threshold=threshold).cap()
    else:
        print(
            "The marching cubes algorithm might be rotated compared to your volume data"
        )
        # Apply marching cubes and save to .obj
        if mcubes_smooth:
            smooth = mcubes.smooth(volume)
            vertices, triangles = mcubes.marching_cubes(smooth, 0)
        else:
            vertices, triangles = mcubes.marching_cubes(volume, 0.5)

        #  create mesh
        mesh = Mesh((vertices, triangles))

    # Cleanup and save
    if extract_largest:
        mesh = mesh.extractLargestRegion()

    # decimate
    mesh.decimate(decimate_fraction, method="pro")

    if smooth:
        mesh.smoothLaplacian()

    if obj_filepath is not None:
        write(mesh, str(obj_filepath))

    return mesh
