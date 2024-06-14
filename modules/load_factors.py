import copy

ASCE_7_LRFD_COMBOS = {
    'LC1': {'D': 1.4},

    'LC2a': {'D': 1.2, 'L': 1.6, 'LLR': 0.5}, 
    'LC2b': {'D': 1.2, 'L': 1.6, 'S': 0.5},
    'LC2c': {'D': 1.2, 'L': 1.6, 'R': 0.5},

    'LC3a': {'D': 1.2, 'LLR': 1.6, 'L': 1.0},
    'LC3b': {'D': 1.2, 'LLR': 1.6, 'W': 0.5},
    'LC3c': {'D': 1.2, 'S': 1.6, 'L': 1.0},
    'LC3d': {'D': 1.2, 'S': 1.6, 'W': 0.5},
    'LC3e': {'D': 1.2, 'R': 1.6, 'L': 1.0},
    'LC3f': {'D': 1.2, 'R': 1.6, 'W': 0.5},

    'LC4a': {'D': 1.2, 'W': 1.0, 'L': 1.0, 'LLR': 0.5},
    'LC4b': {'D': 1.2, 'W': 1.0, 'L': 1.0, 'S': 0.5},
    'LC4c': {'D': 1.2, 'W': 1.0, 'L': 1.0, 'R': 0.5},

    'LC5': {'D': 0.9, 'W': 1.0},

    'LC6': {'D': 1.2, 'E': 1.0, 'L': 1.0, 'S': 0.2},

    'LC7': {'D': 0.9, 'E': 1.0}
}

ASCE_7_SERVICE_COMBOS = {
    'LC1': {'D': 1.0},

    'LC2': {'D': 1.0, 'L': 1.0},

    'LC3a': {'D': 1.0, 'LLR': 1.0},
    'LC3b': {'D': 1.0, 'S': 1.0},
    'LC3c': {'D': 1.0, 'R': 1.0},

    'LC4a': {'D': 1.0, 'L': 0.75, 'LLR': 0.75},
    'LC4b': {'D': 1.0, 'L': 0.75, 'S': 0.75},
    'LC4c': {'D': 1.0, 'L': 0.75, 'R': 0.75},

    'LC5a': {'D': 1.0, 'W': 0.6},
    'LC5b': {'D': 1.0, 'E': 0.7},

    'LC6a': {'D': 1.0, 'L': 0.75, 'W': 0.45, 'LLR': 0.75},
    'LC6b': {'D': 1.0, 'L': 0.75, 'W': 0.45, 'S': 0.75},
    'LC6c': {'D': 1.0, 'L': 0.75, 'W': 0.45, 'R': 0.75},

    'LC7': {'D': 1.0, 'L': 0.75, 'E': 0.525, 'S': 0.75},

    'LC8': {'D': 0.6, 'W': 0.6},

    'LC9': {'D': 0.6, 'E': 0.7}
}

# DEAD LOAD, CONSTRUCTION DL, LIVE LOAD, CONSTRUCTION LIVE LOAD
ASCE_7_PRE_COMP_FACTORED_LOADS = {
    'LC1': {'CD': 1.4},

    'LC2': {'CD': 1.2, 'CL': 1.6},
}

ASCE_7_PRE_COMP_SERVICE_LOADS = {
    'LC1': {'CD': 1.0},
    'LC2': {'CD': 1.0, 'CL': 1.0},
}

def factor_load(D_load: float = 0.0, D: float = 0.0, CD_load: float = 0.0, CD: float = 0.0, CL_load: float = 0.0, CL: float = 0.0, L_load: float = 0.0, L: float = 0.0, LLR_load: float = 0.0, LLR: float = 0.0, S_load: float = 0.0, S: float = 0.0, R_load: float = 0.0, R: float = 0.0, W_load: float = 0.0, W: float = 0.0, E_load: float = 0.0, E: float = 0.0) -> float:
    '''
    returns the calculated factored load when given each load case and the corresponding load factor.

    Args:
        D_load (float): DEAD Load intensity, defaults to 0.0
        D (float): DEAD Load factor, defaults to 0.0
        CD_load (float): CONSTRUCTION DEAD Load intensity, defaults to 0.0
        CD (float): CONSTRUCTION DEAD Load factor, defaults to 0.0
        L_load (float): LIVE Load factor, defaults to 0.0
        L (float): LIVE Load intensity, defaults to 0.0
        CL_load (float): CONSTRUCTION LIVE Load intensity, defaults to 0.0
        CL (float): CONSTRUCTION LIVE Load factor, defaults to 0.0
        LLR_load (float): ROOF LIVE LOAD Load factor, defaults to 0.0
        LLR (float): ROOF LIVE LOAD Load intensity, defaults to 0.0
        S_load (float): SNOW Load factor, defaults to 0.0
        S (float): SNOW Load factor, defaults to 0.0
        R_load (float): RAIN Load intensity, defaults to 0.0
        R (float): RAIN Load factor, defaults to 0.0
        W_load (float): WIND Load intensity, defaults to 0.0
        W (float): WIND Load factor, defaults to 0.0
        E_load (float): SEISMIC Load intensity, defaults to 0.0
        E (float): SEISMIC Load factor, defaults to 0.0
    
    Returns:
        (float): factored load resultant
    '''
    factored_load = D_load * D + CD_load * CD + L_load * L + CL_load * CL + LLR_load * LLR + S_load * S + R_load * R + W_load * W + E_load * E
    return factored_load

def max_factored_load(loads: dict, load_combos: dict) -> float:
    '''
    returns the maximum factored load resultant of the provided load dict for the provided load combination dict.

    Args:
        loads (dict): dictionary of applied loads with keys defining the load case and values defining the load intensity. For example, {'D_load': 175, 'L_load': 20}
        load_combos (dict[str, dict[str, float]]): dictionary of combinations to be considered for determining the max factored load. Refer to combinations in load_factors.py.

    Returns:
        (float): Value of maximum factored load of all combinations.
    '''
    factored_loads = []
    for combo_name, combo in load_combos.items():
        cur_loads = loads | combo # merge the loads dict with the current combo dict.
        factored_load = factor_load(**cur_loads)
        factored_loads.append(factored_load)

    max_load = max(*factored_loads)

    return max_load

def min_factored_load(loads: dict, load_combos: dict) -> float:
    '''
    returns the minimum factored load resultant of the provided loading and load combinations

    Args:
        loads (dict): dictionary of applied loads with keys defining the load case and values defining the load intensity. For example, {'D_load': 175, 'L_load': 20}
        load_combos (dict[str, dict[str, float]]): dictionary of combinations to be considered for determining the min factored load. Refer to combinations in load_factors.py.

    Returns:
        (float): Value of minimum factored load of all combinations.
    '''
    factored_loads = []
    for combo_name, combo in load_combos.items():
        cur_loads = loads | combo # merge the loads dict with the current combo dict.
        factored_load = factor_load(**cur_loads)
        factored_loads.append(factored_load)

    min_load = min(*factored_loads)

    return min_load

def envelope_max(results_arrays: dict) -> list[list[float], list[float]]:
    '''
    Returns a list of lists where the first sublist is the x coordinates along the length of a member and the second sublist is an array of maximum values across all load combinations for each coordinate step.

    Args:
        results_arrays (dict): dictionary of result array, keyed by load combo name (i.e. the output type of beams.extract_arrays_all_combos)

    Returns:
        list[list[float], list[float]]: a list of lists where the first sublist is the x coordinates along the length of a member and the second sublist is an array of maximum values across all load combinations for each coordinate step
    '''
    results_arrays_copy = copy.deepcopy(results_arrays)
    first_key = list(results_arrays_copy.keys())[0]
    x_coords = results_arrays_copy[first_key][0]

    max_force_env = results_arrays_copy[first_key][1]
    for key in results_arrays_copy:
        cur_force_arr = results_arrays_copy[key][1]
        for idx, value in enumerate(cur_force_arr):
            if abs(max_force_env[idx]) < abs(value):
                max_force_env[idx] = value

    max_envelope = [x_coords, max_force_env]

    return max_envelope

def envelope_min(results_arrays: dict) -> list[list[float], list[float]]:
    '''
    Returns a list of lists where the first sublist is the x coordinates along the length of a member and the second sublist is an array of minimum values across all load combinations for each coordinate step.

    Args:
        results_arrays (dict): dictionary of result array, keyed by load combo name (i.e. the output type of beams.extract_arrays_all_combos)

    Returns:
        list[list[float], list[float]]: a list of lists where the first sublist is the x coordinates along the length of a member and the second sublist is an array of minimum values across all load combinations for each coordinate step
    '''
    results_arrays_copy = copy.deepcopy(results_arrays)
    first_key = list(results_arrays_copy.keys())[0]
    x_coords = results_arrays_copy[first_key][0]

    min_force_env = results_arrays_copy[first_key][1]
    for key in results_arrays_copy:
        cur_force_arr = results_arrays_copy[key][1]
        for idx, value in enumerate(cur_force_arr):
            if abs(min_force_env[idx]) > abs(value):
                min_force_env[idx] = value

    min_envelope = [x_coords, min_force_env]

    return min_envelope
