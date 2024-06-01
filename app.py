import streamlit as st
import comp_beam
from steelpy import aisc

w_shapes_list = list(aisc.W_shapes.sections.keys())[::-1]

st.header('Composite Beam Design')

with st.sidebar.expander(label='Span Definition', expanded=True):
    beam_length = st.number_input('Beam Length (ft)', min_value=1, value=30, key='beam_length')
    beam_section = st.selectbox(label='Beam Section', options=w_shapes_list, index=108, key='beam_section')
    beam_fy = st.number_input('Yield Stress (ksi)', value=50, step=5, key='beam_fy')
    shored = st.checkbox('Beam Shored', key='shored')

with st.sidebar.expander(label='Beam Layout', expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        trib_left = st.number_input(label='Distance left (ft)', key='left_dist')
        left_cond = st.selectbox('Dist to Edge or Beam?', ['Beam', 'Edge'], key='left_cond')
        
    with col2:
        trib_right = st.number_input(label='Distance right (ft)', key='right_dist')
        right_cond = st.selectbox('Dist to Edge or Beam?', ['Beam', 'Edge'], key='right_cond')

with st.sidebar.expander(label='Stud Information', expanded=True):
    stud_fu = st.number_input(label='Fu (ksi)', value=65, step=5, key='stud_fu')
    stud_dia = st.selectbox(label='Diameter', options=['3/4"', '5/8"', '1/2"'], key='stud_dia')
    stud_length = st.number_input(label='Length (in)', value=4.0, step=0.5, key='stud_length')

# Deck and Fill
with st.sidebar.expander(label='Deck and Fill', expanded=True):
    conc_thickness = st.number_input(label='Conc thickness above flutes (in)', value=4.0, step=0.5, key='conc_thickness')
    fc = st.number_input(label='Conc strength (ksi)', value=4.0, step=0.5, min_value=3.0, max_value=10.0, key='fc')
    lightweight = st.checkbox('Lightweight', key='lightweight')
    deck_dir = st.selectbox(label='Deck Direction (deg)', options=[0,90], key='deck_dir')
    deck_height = st.number_input(label='Height of deck (in)', value=1.5, step=0.5, key='deck_height')

# Uniform Loading
with st.sidebar.expander(label='Uniform Loads', expanded=True):
    format_str = '%.3f'
    uniform_dead = st.number_input(label='Dead Load (kip/ft)', format=format_str, key='uniform_dead')
    uniform_const_dead = st.number_input(label='Construction Dead Load (kip/ft)', format=format_str, key='uniform_const_dead')
    uniform_live = st.number_input(label='Live Load (kip/ft)', format=format_str, key='uniform_live')
    uniform_partition_live = st.number_input(label='Partion Live Load (kip/ft)', format=format_str, key='uniform_partition_live')
    uniform_const_live = st.number_input(label='Construction Live Load (kip/ft)', format=format_str, key='uniform_const_live')

st.write(st.session_state)

calc_data = comp_beam.calc_beam(st.session_state)

st.write(calc_data)






        


