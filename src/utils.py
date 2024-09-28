import os
import streamlit as st
from neo4j import GraphDatabase

def set_openai_api_key():
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    os.environ["OPENAI_API_KEY"] = openai_api_key

def set_neo4j_connection():
    neo4j_uri = st.secrets["neo4j_uri"]
    neo4j_username = st.secrets["neo4j_username"]
    neo4j_password = st.secrets["neo4j_password"]
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    return driver