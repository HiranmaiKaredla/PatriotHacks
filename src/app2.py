
import streamlit as st
from st_files_connection import FilesConnection
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import re
import pandas as pd
import os
#from config import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = st.scrects['OPENAI_API_KEY']
st.header("PatriotHacks - Dream Home")

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
    sql_query = chain.invoke({"question": "Get ids of {query} limit 10".format(query=text_input)})
    #print(sql_query)
    response = db.run(sql_query)
    #print(response)
    id_numbers = [int(num) for num in re.findall(r'\d+', response)]
    if len(id_numbers):
        filtered_df = df[df['id'].isin(id_numbers)]
        # st.dataframe(filtered_df[['title', 'body', 'amenities', 'bathrooms', 'bedrooms', 'price', 'square_feet', 'cityname', 'state']]
        #     )
        for index, row in filtered_df.iterrows():
            # Create a button for each property
            if st.button(f"{row['title']} - ${row['price']}", key=row['id']):
                # Display detailed information when the button is clicked
                st.subheader(f"Details for {row['title']}")
                st.write(f"Category: {row['category']}")
                st.write(f"City: {row['cityname']}")
                st.write(f"Bedrooms: {row['bedrooms']}, Bathrooms: {row['bathrooms']}")
                st.write(f"Amenities: {row['amenities']}")
                st.write(f"Price: ${row['price']}")
                st.write(f"Property ID: {row['id']}")
    else:
        st.write("Sorry! we done have any results with the query")






