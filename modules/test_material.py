from material import Concrete
import math

conc_material1 = Concrete(
    name = 'My Concrete',
    poisson_ratio = 0.2,
    density = 150,
    fc = 4,
    fy = 60,
    fyt = 60,
    lw_mod_factor = 1.0,
)

def test_Ec():
    assert math.isclose(conc_material1.Ec, 3834.25, rel_tol=0.1)