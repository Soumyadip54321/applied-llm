'''
Script that creates an UI that displays restaurant name and possible menus using agentic AI.
'''

import streamlit as st
from backend.restaurant_and_menu_generator_server import generate_restaurant_and_menu

st.title('Fictitious Restaurant with Menu Generator')

# choose cuisine
cuisine = st.sidebar.selectbox('Pick a cuisine',options=["Indian","Italian","Nepalese","Chinese","Japanese","Mongolian","American","Mexican","Finnish","Greenlandish"],help="Choose a cuisine")

if cuisine:
    response = generate_restaurant_and_menu(cuisine)
    # display restaurant name
    restaurant = response['restaurant_name']
    # result = re.findall(pattern=r'\*\*(.*?)\*\*',string=restaurant)
    st.header(restaurant)
    # fetch menu items
    menu_items = response['menu'].split(',')

    # display menu items
    with st.container(border=True):
        st.subheader('Menu items')

        for item in menu_items:
            st.write('-',item)






