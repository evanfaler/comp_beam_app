from dataclasses import dataclass
from modules.material import Material, Steel
from steelpy.steelpy import Section
import modules.load_factors as load_factors
from math import sqrt
import copy
from PyNite import FEModel3D

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
    fea_beam: FEModel3D = None

    def __post_init__(self): # calculated parameters after dataclass initialization
        # Calculate and store factored load dictionaries
        self.factored_loads = {
            'pre_comp_factored': self.generate_factored_loads(load_factors.ASCE_7_PRE_COMP_FACTORED_LOADS),
            'pre_comp_service': self.generate_factored_loads(load_factors.ASCE_7_PRE_COMP_SERVICE_LOADS),
            'comp_factored': self.generate_factored_loads(load_factors.ASCE_7_LRFD_COMBOS),
            'comp_service': self.generate_factored_loads(load_factors.ASCE_7_SERVICE_COMBOS)
        }

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
    
    def calc_req_steel_area(self) -> float:
        '''
        Calculates the required steel area needed (in^2) for the beam section, assuming that PNA is in the slab. Used for initial sizing of beam before iterative calculations are completed.
        '''
        Mu = self.fea_beam.Members[self.name].max_moment('Mz', combo_name='comp_factored') * 12 #convert to kip*inches
        phi = 0.9
        Fy = self.steel_material.fy
        d = self.shape.d
        ts = self.deck['t_s']
        a = 1 # Assumed 1in deep for preliminary design. See Salmon & Johnson chapter 16.10.

        A_s = Mu / (phi * Fy * ((d/2) + ts - a/2))

        return A_s
    
    def calc_pre_comp_strength(self) -> float:
        '''
        Calculates and returns the pre-composite strength of the beam.
        '''
        if self.deck['orientation'] == 0:
            # Deck oriented parallel to beam. Beam is only braced at perpendicular framing members.
            #TODO: add logic for this case.
            pass
        elif self.deck['orientation'] == 90:
            #Deck oriented perpendicular to beam, top flange is braced continuously

            pass

    

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

    def web_is_compact(self) -> bool:
        '''
        Returns whether steel shape web is compact or not.
        '''
        h_tw = self.shape.T / self.shape.tw
        if h_tw <= 3.76 * sqrt(self.steel_material.E / self.steel_material.fy): # web is compact
            return True
        else:
            return False
        
    def flange_is_compact(self) -> bool:
        '''
        Returns whether steel shape flange is compact or not.
        '''
        b_t = (self.shape.bf / 2) / self.shape.tf
        if b_t <= 0.38 * sqrt(self.steel_material.E / self.steel_material.fy): # flange is compact
            return True
        else: 
            return False

    def generate_factored_loads(self, load_combos: dict) -> float:
        '''
        Returns a factored load dict based on the selected load_combination. Refer to load_factors.py for load_combination choices.
        
        Parameters:
            load_combinations (dict): dictionary of load combinations to use for factoring. Must match one of the combinations in load_factors.py.

        Returns:
            (dict): modified load dictionary with load intensities modified to be the resultant of the maximum load case.
        '''
        
        # Uniformly distributed loads
        load_dict = {}
        for load in self.loads:
            if load.load_case == 'D' or load.load_case == 'CD': # add beam self weight to DL case.
                load_dict[f'{load.load_case}_load'] = load.magnitude + self.shape.weight / 1000
            else:
                load_dict[f'{load.load_case}_load'] = load.magnitude
        
        factored_UDL = load_factors.max_factored_load(load_dict, load_combos=load_combos)

        # Combine into one load dict
        factored_loads = {
            'UDL': factored_UDL
        }

        return factored_loads
    
    def analyze(self):
        '''
        Generates, analyzes and returns a Pynite FEA model from the properties of the object.
        '''
        # Create a new finite element model
        beam = FEModel3D()

        # Add nodes (14 ft = 168 inches apart)
        beam.add_node('N1', 0, 0, 0)
        beam.add_node('N2', self.span, 0, 0)

        # Define a material
        E = self.steel_material.E               # Modulus of elasticity (ksi)
        G = self.steel_material.G               # Shear modulus of elasticity (ksi)
        nu = self.steel_material.poisson_ratio  # Poisson's ratio
        rho = self.steel_material.density / (1000 * 12**3)  # Density (kci)
        beam.add_material('Steel', E, G, nu, rho)

        # Add beam with appropriate properties
        beam.add_member(name=self.name, i_node='N1', j_node='N2', material_name='Steel', Iy=self.shape.Iy, Iz=self.shape.Ix, J=self.shape.J, A=self.shape.area)

        # Provide simple supports
        beam.def_support('N1', True, True, True, False, False, False)
        beam.def_support('N2', True, True, True, True, False, False)

        # Add uniform loads
        for case_name in self.factored_loads:
            # Add each type of load to analysis member
            # UDLs      
            udl_magnitude = self.factored_loads[case_name]['UDL']
            udl_start = 0
            udl_stop = self.span
            beam.add_member_dist_load(member_name=self.name, Direction='Fy', w1=udl_magnitude, w2=udl_magnitude, x1=udl_start, x2=udl_stop, case=case_name)
            
            # Add load combos that are just a 1.0 factor for each load case, named the same as the load case.
            beam.add_load_combo(name=case_name, factors={f'{case_name}': 1.0})
        

        # Run analysis on beam.
        beam.analyze_linear()

        # Assign to fea_analysis property. Results may be queried from other methods using self.fea_beam now.
        self.fea_beam = beam