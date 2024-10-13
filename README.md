# PatriotHacks

## Inspiration
The housing crisis in the U.S. inspired me to develop a solution that addresses both affordability and sustainability. Rising home prices, climate change, and the need for housing that aligns with people's lifestyles and budgets motivated me to create a tool that uses data to bridge these gaps.

## What It Does
HomeMap is a tool that matches buyers and renters with affordable, sustainable homes based on publicly available housing and demographic data. It also considers environmental factors like climate resilience to help users make informed decisions about where to live. The tool provides insights into housing supply and affordability, aiding first-time home buyers and those seeking environmentally conscious housing.

## How We Built It
The project was built using Python and integrated with Azure for scalable data processing. I used PySpark to handle large datasets efficiently, and machine learning models like Random Forest for classification and XGBoost for regression tasks. The Google Maps API helped add location-based context, while Text to SQL was used to query and process the data. Streamlit provided an interactive web interface, and Tableau was used for data visualization to present results in a user-friendly format.

## Challenges We Ran Into
The biggest challenge was finding suitable datasets. Many datasets were either incomplete or unavailable, which made data collection and cleaning time-consuming. Integrating data from different sources—such as demographics, housing transactions, and climate data—was also complex. Additionally, balancing model performance with the scale of data processing was an ongoing challenge.

## Accomplishments That We're Proud Of
We successfully built a functioning tool that uses multiple data sources to deliver insights on housing affordability and sustainability. The integration of machine learning models like Random Forest and XGBoost allowed us to provide predictions that help users make more informed decisions. We're also proud of the intuitive interface, making the tool accessible for non-technical users.

## What We Learned
We learned a great deal about processing and integrating large, diverse datasets, and how to effectively apply machine learning models to real-world problems. We also gained experience in building scalable solutions using Azure and PySpark. Finally, working through challenges with data availability helped us improve our data wrangling and pipeline development skills.

## What's Next for HomeMap
Next steps for HomeMap include incorporating more datasets to improve the accuracy of our predictions, especially around housing supply and climate impact. We also plan to enhance the user interface and add more customization options for users, allowing them to filter results based on specific preferences. Expanding the tool to cover more regions and offer deeper insights on housing trends is also on the roadmap.

## Tasks Performed

## Tasks Performed

- Scouted and scraped housing data, including amenities
- Generated geospatial data based on zip codes
- Integrated Google Maps to find nearby essentials (schools, hospitals, etc.)
- Predicted house prices using machine learning models
- Estimated house evaluation metrics
- Developed Text-to-SQL generation for natural language queries
- Implemented Named Entity Recognition (NER) for data extraction
- Built a user-friendly interface with Streamlit
