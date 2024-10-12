
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import re
import pandas as pd
import os
from config import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

df = pd.read_csv("./apartments_for_rent_classified_10K.csv", encoding="latin-1", sep=";")
engine = create_engine("sqlite:///properties.db")
try:
    df.to_sql("properties", engine, index=False)
except:
    print("DB not created")

llm = ChatOpenAI(model="gpt-3.5-turbo")
db = SQLDatabase.from_uri("sqlite:///properties.db")

chain = create_sql_query_chain(llm, db)

text_input = st.text_input("Enter your query")

if text_input:
    sql_query = chain.invoke({"question": "Get ids of {query}".format(query=text_input)})
    response = db.run(sql_query)
    
    id_numbers = [int(num) for num in re.findall(r'\d+', response)]
    filtered_df = df[df['id'].isin(id_numbers)]
    st.dataframe(filtered_df)





