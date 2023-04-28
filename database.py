import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta


# Load the environment variables
DETA_KEY = st.secrets["DETA_KEY"]

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("chat_bot")


def insert_data(query, response):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"query": query, "response": response})


def fetch_all_periods():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items


def get_period(period):
    """If not found, the function will return None"""
    return db.get(period)