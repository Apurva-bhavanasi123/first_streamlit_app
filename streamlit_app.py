import snowflake.connector
import streamlit
from urllib.error import URLError
import requests
import pandas
streamlit.title("My Parents New Healthy Diner")

streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Strawberries','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if(not fruit_choice):
    streamlit.error("Please select a fruit to get information")
  else:
    streamlit.write('The user entered ', fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    #streamlit.text(fruityvice_response.json())
    # Normalises data
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # writes table
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("Fruit load list contains ")
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input('What fruit would you like to add?','Kiwi')
streamlit.write('Thanks for adding', add_my_fruit)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
