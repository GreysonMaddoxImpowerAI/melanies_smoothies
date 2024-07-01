# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe
)

customer_name = st.text_input(
    'Input customer name here: '
)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fv_df = st.dataframe(data= fruityvice_response.json(), use_container_width=True) 

if ingredients_list:
    ingredients_string = ' and '.join(ingredients_list)
    my_insert_stmt = f"""insert into smoothies.public.orders(name_on_order, ingredients)
        values ('{customer_name}', '{ingredients_string}')"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
