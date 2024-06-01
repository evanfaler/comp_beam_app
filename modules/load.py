from dataclasses import dataclass

@dataclass
class Load():
    '''
    Load class

    Parameters
        name (str) Optional = None: user defined description for load.
        load_case (str): type of load e.g. D, L, LLr
    '''
    name: str
    load_case: str

@dataclass
class UniformLoad(Load):
    '''
    Uniform load class, extends Load

    Parameters:
        magnitude (float): Magnitude of the uniform load, klf
        start_loc (float): Starting location of uniform load, ft
        end_loc (float): Ending location of uniform load, ft
    '''
    magnitude: float
    start_loc: float
    end_loc: float