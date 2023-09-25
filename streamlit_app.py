import streamlit
import requests
import pandas as pd
import snowflake.connector
from urllib.error import URLError

cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])


def get_fruity_vice_date(fruit_choice):
    fruityvice_response = requests.get(
        "https://fruityvice.com/api/fruit/" + fruit_choice
    )
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


def get_fruit_load_list():
    with cnx.cursor() as cur:
        cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return cur.fetchall()


def insert_row_snowflake(new_fruit):
    with cnx.cursor() as cur:
        cur.execute(f"INSERT INTO FRUIT_LOAD_LIST VALUES ('{new_fruit}')")
        return "Thanks for adding " + new_fruit


streamlit.title("My Parents New Healthy Diner")

streamlit.header("Breakfast Favorites")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")

my_fruit_list = pd.read_csv(
    "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
)
my_fruit_list = my_fruit_list.set_index("Fruit")

fruits_selected = streamlit.multiselect(
    "Pick some fruits:", list(my_fruit_list.index), ["Avocado", "Strawberries"]
)
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input("What fruit would you like information about?")
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        fruityvice_normalized = get_fruity_vice_date(fruit_choice)
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()

streamlit.header("The fruit load list contains:")
if streamlit.button("Get Fruit Load List"):
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


add_my_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button("Add Fruit Load List"):
    streamlit.text(insert_row_snowflake(add_my_fruit))
