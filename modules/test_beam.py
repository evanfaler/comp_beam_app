from modules.material import Concrete, Steel
from modules.beam import CompositeSteelBeam
from modules.load import UniformLoad
from steelpy.steelpy import aisc

test_beam1 = CompositeSteelBeam(
    name='Composite Beam 1', 
    span=30, 
    shape=aisc.W_shapes.W16X26, 
    shored=False, 
    layout=(('Beam', 8.0), ('Beam', 8.0)), 
    studs={'fu': 65, 'dia': 0.75, 'length': 5.0, 'max_comp': 1.0, 'min_comp': 0.25}, 
    deck={'t_s': 3.5, 'deck_height': 3.0, 'orientation': 90}, 
    steel_material=Steel(
        name='Steel', 
        poisson_ratio=0.3, 
        density=490, 
        E=29000, 
        G=11200, 
        fy=50, 
        fu=65), 
    concrete_material=Concrete(
        name='Concrete', 
        poisson_ratio=0.2, 
        density=145, 
        fc=4.0, 
        fy=60, 
        fyt=60, 
        lw_mod_factor=1.0), 
    loads=[
        UniformLoad(name='Uniform Dead Load', load_case='D', magnitude=0.5, start_loc=0, end_loc=30), 
        UniformLoad(name='Uniform Construction Dead Load', load_case='CD', magnitude=0.5, start_loc=0, end_loc=30), 
        UniformLoad(name='Uniform Live Load', load_case='L', magnitude=1.3, start_loc=0, end_loc=30), 
        UniformLoad(name='Uniform Construction Live Load', load_case='CL', magnitude=0.2, start_loc=0, end_loc=30)], 
    fea_beam=None)