from modules.beam import CompositeSteelBeam
from modules.load import UniformLoad
from steelpy import aisc
from modules.material import Steel, Concrete

def generate_loads(data: dict) -> list:
    '''
    Generates a list of loads from the provided streamlit session data

    Parameters:
        data (dict): streamlit session_state dictionary of all data.

    Returns:
        list: list of Loads applied to the beam.
    '''
    loads = []

    # Uniform Loads
    loads.append(UniformLoad(
        name = 'Uniform Dead Load',
        load_case = 'D',
        magnitude = data['uniform_dead'],
        start_loc = 0,
        end_loc = data['beam_length'],
    ))

    loads.append(UniformLoad(
        name = 'Uniform Construction Dead Load',
        load_case = 'CD',
        magnitude = data['uniform_const_dead'],
        start_loc = 0,
        end_loc = data['beam_length'],
    ))

    loads.append(UniformLoad(
        name = 'Uniform Live Load',
        load_case = 'L',
        magnitude = data['uniform_live'],
        start_loc = 0,
        end_loc = data['beam_length'],
    ))

    loads.append(UniformLoad(
        name = 'Uniform Partition Live Load',
        load_case = 'Lp',
        magnitude = data['uniform_partition_live'],
        start_loc = 0,
        end_loc = data['beam_length'],
    ))

    loads.append(UniformLoad(
        name = 'Uniform Construction Live Load',
        load_case = 'CL',
        magnitude = data['uniform_const_live'],
        start_loc = 0,
        end_loc = data['beam_length'],
    ))

    return loads

def str_fraction_to_float(fraction: str) -> float:
    '''
    Converts fractional string including inches symbol and returns decimal
    
    Parameters:
        fraction (str): string including fraction and inches symbol e.g. 3/4"
    
    Returns:
        float: decimal representation of the provided string.
    '''
    fraction = fraction.replace('"','').replace('\'','')
    fraction_answer = eval(fraction.strip().replace(" ", "+"))
    return fraction_answer  
    
def generate_comp_beam(data: dict) -> CompositeSteelBeam:
    '''
    Generates a CompositeSteelBeam object from the streamlit session data

    Parameters:
        data (dict): streamlit session_state dictionary of all data.

    Returns:
        CompositeSteelBeam: CompositeSteelBeam object ready for analysis and data querying.

    '''

    studs = {
        'fu': data['stud_fu'],
        'dia': str_fraction_to_float(data['stud_dia']),
        'length': data['stud_length']
        }
    
    deck = {
        't_s': data['conc_thickness'],
        'deck_height': data['deck_height'],
        'orientation': data['deck_dir'],
    }
    
    loads = generate_loads(data)

    steel_material = Steel(
        name='Steel',
        poisson_ratio=0.3,
        density=490,
        E=29000,
        fy=data['beam_fy'],
        fu=65
    )

    conc_material = Concrete(
        name='Concrete',
        poisson_ratio=0.2,
        density=150,
        fc=data['fc'],
        lw_mod_factor = 0.75 if data['lightweight'] else 1.0
    )
    
    beam = CompositeSteelBeam(
        name = 'Composite Beam',
        span=data['beam_length'],
        shape=getattr(aisc.W_shapes, data['beam_section']),
        shored=data['shored'],
        layout=((data['left_cond'], data['left_dist']), (data['right_cond'], data['right_dist'])),
        studs=studs,
        deck=deck,
        steel_material=steel_material,
        concrete_material=conc_material,
        loads=loads        
    )
    
    return beam

def calc_beam(data: dict) -> dict:
    '''
    Calculates beam capacity and returns dictionary of outputs to be added to Streamlit App
    '''
    comp_beam = generate_comp_beam(data)
    print(comp_beam)
    
    return comp_beam
    




