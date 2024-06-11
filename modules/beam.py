from dataclasses import dataclass
from modules.material import Material, Steel
from steelpy.steelpy import Section
from math import sqrt

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
    
    def modular_ratio(self) -> float:
        '''
        Returns the modular ratio, n, of the composite beam
        '''
        return self.steel_material.E / self.concrete_material.Ec
    
    #TODO: finish PNA method
    def calc_PNA(self) -> float:
        '''
        Returns the location of the plastic nuetral axis, measured from top of the slab
        '''
        if self.deck['orientation'] == 0:
            # Deck oriented parallel to beam
            #TODO: add logic for this case.
            pass
        elif self.deck['orientation'] == 90:
            # Deck oriented perpendicular to beam. Concrete in ribs, that is below the top of the deck, is neglected in determining section properties.
            n = self.modular_ratio()
            beff_mod = self.calc_effective_width() * 12 / n
            print(f'Effective width: {self.calc_effective_width()*12} in')
            print(f'{beff_mod=}')
            
            # Calc y_bar
            transformed_conc_area = beff_mod * self.deck['t_s']
            transformed_conc_y = self.deck['t_s'] / 2
            steel_area = self.shape.area
            steel_y = self.deck['t_s'] + self.deck['deck_height'] + self.shape.d / 2
            y_bar = sum([transformed_conc_area*transformed_conc_y, steel_area*steel_y]) / sum([transformed_conc_area, steel_area])

            print(f'{transformed_conc_area=}')
            print(f'{transformed_conc_y=}')
            print(f'{steel_area=}')
            print(f'{steel_y=}')
            print(f'{y_bar=}')

            
            pass

    def calc_full_comp_moment_capacity(self) -> float:
        '''
        Returns the full composite moment capacity of the composite beam in kip-ft.
        '''
        C = self.calc_full_comp_C()
        a = self.calc_stress_block_depth(C)
        y = (self.shape.d / 2) + (self.deck['t_s'] + self.deck['deck_height']) - (a / 2)
        phi_Mn = 0.9 * C * y / 12

        return phi_Mn

    def calc_full_comp_C(self) -> float:
        '''
        Returns the controlling force (kips) required for full composite action.
        '''
        beff = self.calc_effective_width() * 12

        if self.deck['orientation'] == 0:
            # Deck oriented parallel to beam
            #TODO: add logic for this case.
            conc_area = None
        elif self.deck['orientation'] == 90:
            # Deck perpendicular to beam
            conc_area = beff * self.deck['t_s']

        steel = self.shape.area * self.steel_material.fy
        concrete = 0.85 * self.concrete_material.fc * conc_area

        return min([steel, concrete])

    def calc_stress_block_depth(self, force: float, b: float = None) -> float:
        '''
        Calculates stress block depth in inches, a, of concrete for the provided force in kips

        Parameters:
            force: compressive force in concrete, kips
            b: width of concrete slab to be considered in inches, typically beff. Defaults to calculated beff.

        Returns:
            float: compression block depth, a, in inches.
        '''
        if b == None:
            b = self.calc_effective_width() * 12

        return force / (0.85 * self.concrete_material.fc * b)

    def is_web_compact(self) -> bool:
        '''
        Returns whether steel shape web is compact or not.
        '''
        h_tw = self.shape.T / self.shape.tw
        if h_tw <= 3.76 * sqrt(self.steel_material.E / self.steel_material.fy): # section is compact
            return True
        else:
            return False

    
    
    


    




