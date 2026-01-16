# Import python packages
import streamlit as st
##from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!
  """)

name_on_order = st.text_input("Name on smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

#option = st.selectbox(
#    "What is your favorite fruit?",
##   ("Banana", "Strawberries", "Peaches"))

#st.write("Your favorite fruit is:", option)

##session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
##显示所有column是这样：
#my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#显示表的内容在屏幕上
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
    )
if ingredients_list:
    ##st.write(ingredients_list)
    ##st.text(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)
    
####Python标准要求是用4个空格作为一级缩进，tab键通用性不好
## for fruit_chosen in ingredients_list:
##which actually means...
##for each fruit_chosen in ingredients_list multiselect box: do everything below this line that is indented. 
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','"""+name_on_order+ """');"""
    ##把生成的insert的sql语句显示在屏幕上
    
    ##st.write(my_insert_stmt)
##  stop here, will not insert.    
##    st.stop()
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered,'+name_on_order+'!', icon="✅")

##new section to display smoothiefroot nutrion information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
