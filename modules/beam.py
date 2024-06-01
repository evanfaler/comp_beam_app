from dataclasses import dataclass
from modules.material import Material, Steel
from steelpy.steelpy import Section

@dataclass
class Beam:
    name: str
    span: float

@dataclass
class CompositeSteelBeam(Beam):
    '''
    Composite steel beam class

    Parameters:
        shape (Section): SteelPy Section object of the steel beam.
        shored (bool): Boolean on if beam is shored during construction or not.
        layout ((str, float), (str, float)): nested tuple indicating distance to adjacent edge or beam. Left side of beam is first, right side is second.
        studs (dict): dictionary of stud information in the following form:
            {
            'fu': float,
            'dia': float,
            'length': float
            }
        deck (dict): dictionary of slab and deck information
            {
            't_s': float,
            'deck_height': float,
            'orientation': float,
            }
        conc_material (Material): concrete slab material properties
        loads (list) Optional = []: list of Load objects defining all loads applied to the beam. Defaults to empy list.
    '''
    shape: Section
    shored: bool
    layout: tuple
    studs: dict
    deck: dict
    steel_material: Material
    concrete_material: Material
    loads: list

    def __post_init__(self): # calculated parameters after dataclass initialization
        pass

    def calc_effective_width(self) -> float:
        '''
        Returns the effective width of the beam in feet
        '''
        #TODO: write test function for effective beam width.
        left_cond = self.layout[0][0]
        left_dist = self.layout[0][1]
        right_cond = self.layout[1][0]
        right_dist = self.layout[1][1]

        beff_left = min(
            self.span / 8,
            left_dist / 2 if left_cond == 'Beam' else left_dist
        )

        beff_right = min(
            self.span / 8,
            right_dist / 2 if right_cond == 'Beam' else right_dist
        )

        return (beff_left + beff_right)
    
    #TODO: finish this function. Need to review textbook to calculate correctly.
    def calc_compressive_force(self) -> float:
        steel_force = self.steel_material.fy * self.shape.area
        concrete_force = 0.85 * self.concrete_material.fc

        print(f'{steel_force=}')
        print(f'{concrete_force=}')
        # compression = min(
        #     self.steel_material.fy * self.shape.area
        # )
        pass

    




