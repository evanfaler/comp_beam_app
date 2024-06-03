from dataclasses import dataclass
from math import sqrt

@dataclass
class Material:
    '''
    General Material Class

    Parameters
        name (str): Name of the material
        poisson_ratio (float): Poisson's ratio of the material
        density (float): Material density, lb/ft3
    '''
    name: str
    poisson_ratio: float
    density: float

@dataclass
class Steel(Material):
    '''
    Steel material class

    Parameters:
        E: (int) Optional = 29000: Modulus of elasticity of steel, ksi
        fy: (int) Optional = 50: Minimum yield stress of steel, ksi
        fu: (int) Optional = 65: Tensile stress, ksi
    '''
    E: int = 29000
    fy: int = 50
    fu: int = 65

@dataclass
class Concrete(Material):
    '''
    Concrete material class

    Parameters:
        fc: (float) Optional = 4.0: Compressive strength of concrete, ksi
        fy: (int) Optional = 60: Yield strength of longitudinal reinforcing, ksi
        fyt: (int) Optional = 60: Yield strength of transverse reinforcing, ksi
        lw_mod_factor (float) Optional = 1.0: lightweight modification factor per ACI.

    Calculated Values:
        Ec: float: Modulus of elasticity of concrete (ksi), calculated per ACI 318-19 eq. 19.2.2.1(a)
    '''
    fc: float = 4.0
    fy: int = 60
    fyt: int = 60
    lw_mod_factor: float = 1.0
    
    def __post_init__(self): # calculated parameters after dataclass initialization
        self.Ec = (self.density**1.5)*33*sqrt(self.fc*1000) / 1000
    
