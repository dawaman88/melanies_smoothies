# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.data_frame(data=smootiefroot_reponse.json(),use_container_width=True)
# Write directly to the app
st.title(f"Customize your Smoothie: :mate_drink:")
st.write(
  """Choose the fruits you want in your custom Smoothie!!.
  """
)


# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

name_order = st.text_input('Name of the Smoothie')
st.write('name of the smoothie is ',name_order)



ingredients_list = st.multiselect('Choose up to 5 Ingredients:',my_dataframe,max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''

    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_order + """')"""

    time_to_insert = st.button('Submit Order')

    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    

#st.dataframe(data=my_dataframe, use_container_width=True)
