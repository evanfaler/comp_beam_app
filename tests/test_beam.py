from modules.beam import CompositeSteelBeam
from modules.load import UniformLoad
from modules.material import Steel, Concrete
from steelpy import aisc
import math

test_beam = CompositeSteelBeam(
    name='Composite Beam', 
    span=30, 
    shape=aisc.W_shapes.W12X26, 
    shored=False, 
    layout=(('Beam', 8.0), ('Beam', 8.0)), 
    studs={'fu': 65, 'dia': 0.75, 'length': 4.0}, 
    deck={'t_s': 4.0, 'deck_height': 1.5, 'orientation': 0}, 
    steel_material=Steel(
        name='Steel', 
        poisson_ratio=0.3, 
        density=490, 
        E=29000, 
        fy=50, 
        fu=65), 
    concrete_material=Concrete(
        name='Concrete', 
        poisson_ratio=0.2, 
        density=150, 
        fc=4.0, 
        fy=60, 
        fyt=60, 
        lw_mod_factor=1.0), 
    loads=[
        UniformLoad(
            name='Uniform Dead Load', 
            load_case='D', 
            magnitude=0.0, 
            start_loc=0, 
            end_loc=30), 
        UniformLoad(
            name='Uniform Construction Dead Load', 
            load_case='CD', 
            magnitude=0.0, 
            start_loc=0, 
            end_loc=30), 
        UniformLoad(
            name='Uniform Live Load', 
            load_case='L', 
            magnitude=0.0, 
            start_loc=0, 
            end_loc=30), 
        UniformLoad(
            name='Uniform Partition Live Load', 
            load_case='Lp',
            magnitude=0.0, 
            start_loc=0, 
            end_loc=30), 
        UniformLoad(
            name='Uniform Construction Live Load', 
            load_case='CL', 
            magnitude=0.0, 
            start_loc=0, 
            end_loc=30)
    ]
)

def test_get_effective_width():
    beff = test_beam.calc_effective_width()

    assert math.isclose(beff, 7.5, rel_tol=0.1)

def test_modular_ratio():
    n = test_beam.modular_ratio()
    
    assert math.isclose(n, 7.56, rel_tol=0.01)