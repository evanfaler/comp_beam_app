import load_factors

def test_factor_load():
    test1 = load_factors.factor_load(20, 1.4)
    test2 = load_factors.factor_load(20, 1.2, 40, 1.6, 20, 0.5)
    test3 = load_factors.factor_load(D_load=20, D=1.2, E_load=-10, E=1.0, L_load=10, L=1.0, S_load=10, S=0.2)
    test4 = load_factors.factor_load(CD_load=20, CD=1.4)
    test5 = load_factors.factor_load(CD_load=20, CD=1.2, CL_load=20, CL=1.6)

    assert test1 == 28
    assert test2 == 98
    assert test3 == 26
    assert test4 == 28
    assert test5 == 56

def test_max_factored_load():
    load1 = {'D_load': 20}
    load2 = {'D_load': 20, 'L_load': 40, 'LLR_load': 20}
    load3 = {'D_load': 20, 'L_load': 40, 'E_load': 20, 'S_load': 10}
    load4 = {'CD_load': 20}
    load5 = {'CD_load': 20, 'CL_load': 20}

    assert load_factors.max_factored_load(load1, load_factors.ASCE_7_LRFD_COMBOS) == 28
    assert load_factors.max_factored_load(load2, load_factors.ASCE_7_LRFD_COMBOS) == 98
    assert load_factors.max_factored_load(load3, load_factors.ASCE_7_LRFD_COMBOS) == 93

    # Testing composite load factores
    assert load_factors.max_factored_load(load4, load_factors.ASCE_7_LRFD_COMBOS) == 0.0 #confirm that composite load factors aren't in typical combos.
    assert load_factors.max_factored_load(load5, load_factors.ASCE_7_LRFD_COMBOS) == 0.0 #confirm that composite load factors aren't in typical combos.
    assert load_factors.max_factored_load(load4, load_factors.ASCE_7_PRE_COMP_FACTORED_LOADS) == 28.0
    assert load_factors.max_factored_load(load5, load_factors.ASCE_7_PRE_COMP_FACTORED_LOADS) == 56.0
    assert load_factors.max_factored_load(load4, load_factors.ASCE_7_PRE_COMP_SERVICE_LOADS) == 20.0
    assert load_factors.max_factored_load(load5, load_factors.ASCE_7_PRE_COMP_SERVICE_LOADS) == 40.0

def test_min_factored_load():
    load1 = {'D_load': 20}
    load2 = {'D_load': 20, 'L_load': 40, 'LLR_load': 20}
    load3 = {'D_load': 20, 'L_load': 40, 'W_load': 50, 'E_load': 60, 'S_load': 10}
    load4 = {'D_load': 20, 'L_load': 40, 'E_load': -20, 'S_load': 10}
    load5 = {'CD_load': 20}
    load6 = {'CD_load': 20, 'CL_load': 20}

    assert load_factors.min_factored_load(load1, load_factors.ASCE_7_LRFD_COMBOS) == 18
    assert load_factors.min_factored_load(load2, load_factors.ASCE_7_LRFD_COMBOS) == 18
    assert load_factors.min_factored_load(load3, load_factors.ASCE_7_LRFD_COMBOS) == 28
    assert load_factors.min_factored_load(load4, load_factors.ASCE_7_LRFD_COMBOS) == -2
    
    # Testing composite load factores
    assert load_factors.min_factored_load(load5, load_factors.ASCE_7_LRFD_COMBOS) == 0.0 #confirm that composite load factors aren't in typical combos.
    assert load_factors.min_factored_load(load6, load_factors.ASCE_7_LRFD_COMBOS) == 0.0 #confirm that composite load factors aren't in typical combos.
    assert load_factors.min_factored_load(load5, load_factors.ASCE_7_PRE_COMP_FACTORED_LOADS) == 24.0
    assert load_factors.min_factored_load(load6, load_factors.ASCE_7_PRE_COMP_FACTORED_LOADS) == 28.0
    assert load_factors.min_factored_load(load5, load_factors.ASCE_7_PRE_COMP_SERVICE_LOADS) == 20.0
    assert load_factors.min_factored_load(load6, load_factors.ASCE_7_PRE_COMP_SERVICE_LOADS) == 20.0