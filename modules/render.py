from PIL import Image, ImageDraw
from beam import CompositeSteelBeam
import numpy as np

def render_beam_isometric(beam: CompositeSteelBeam, img_width: float = 500, img_height: float = 300) -> Image:
    '''
    Creates a 2D isometric image of the provided composite beam.

    Parameters:
        beam (CompositeSteelBeam): CompositeSteelBeam object that describes the composite beam being considered.
        img_width (float) Optional: Image width in pixels
        img_height (float) Optional: Image height in pixels

    Returns:
        Image: Isometric rendering of the beam using Pillow
    '''
    im = Image.new(mode='RGB', size=(500,300), color=(255,223,186))
    draw = ImageDraw.Draw(im)

    return im

def render_beam_section(beam: CompositeSteelBeam, img_width: float = 500, img_height: float = 300) -> Image:
    '''
    Create 2D section image of the composite beam provided.

    Parameters:
        beam (CompositeSteelBeam): CompositeSteelBeam object that describes the composite beam being considered.
        img_width (float) Optional: Image width in pixels
        img_height (float) Optional: Image height in pixels

    Returns:
        Image: 2D Section view of the beam using Pillow
    '''
    # Initialize image and draw
    im = Image.new(mode='RGB', size=(img_width,img_height), color=(255,255,255))
    draw = ImageDraw.Draw(im, mode='RGBA')

    # Generate list of points for steel beam.
    bf = beam.shape.bf
    tf = beam.shape.tf
    tw = beam.shape.tw
    d = beam.shape.d

    steel_beam_coords = [
        (0,0),
        (bf, 0),
        (bf, tf),
        (bf - ((bf - tw )/ 2), tf),
        (bf - ((bf - tw )/ 2), d - tf),
        (bf, d - tf),
        (bf, d),
        (0, d),
        (0, d - tf),
        ((bf - tw) / 2, d - tf),
        ((bf - tw) / 2, tf),
        (0, tf)
    ]

    # Generate list of points for the concrete slab
    slab_depth = beam.deck['deck_height'] + beam.deck['t_s']
    slab_width = beam.calc_effective_width() * 12
    conc_slab_coords = [
        (0,0),
        (slab_width, 0),
        (slab_width, slab_depth),
        (0, slab_depth)
    ]

    #Calculate an appropriate scale to fill the image region
    total_height = d + slab_depth
    scale_x = img_width / slab_width
    scale_y = img_height / total_height
    scale = min(scale_x, scale_y)

    # use numpy to shift slab to be centered, on top of beam then scale everything.
    np_conc_nodes = np.array(conc_slab_coords)
    np_conc_nodes *= scale #scale entire matrix
    np_conc_nodes[:,0] += img_width / 2 - (slab_width / 2) * scale #shift x coords to center in image
    scaled_conc_nodes = list(map(tuple, np_conc_nodes)) #convert nodes back to list of tuples for PIllow

    # Use numpy to scale coords element wise, then convert back to list of tuples for Pillow.
    np_steel_nodes = np.array(steel_beam_coords)
    np_steel_nodes *= scale #scale coordinates
    np_steel_nodes[:,0] += img_width / 2 - (bf /2) * scale #shift x coords to center beam in image.
    np_steel_nodes[:,1] += slab_depth * scale #shift y coords down to make room for slab.
    scaled_steel_nodes = list(map(tuple, np_steel_nodes)) #convert nodes back to list of tuples for PIllow

    # Draw steel shape on image
    line_width = round(min(img_height, img_width) * 0.01)
    draw.polygon(xy=scaled_steel_nodes, outline='red', width=line_width)
    draw.polygon(xy=scaled_conc_nodes, outline='gray', width=line_width, fill='darkgray')

    return im

    






    