import matplotlib
import pandas as pd
import streamlit as st
import numpy as np

def distance_matrix(distance_file,b2b_file):
    distance_df = pd.read_csv(distance_file)
    b2b_df = pd.read_csv(b2b_file)
    distance_df.columns = ['City_Pair', 'Distance']

    b2b_df.set_index("Category", inplace=True)
    # Iterate over the DataFrame to generate the formatted strings
    
    for index, row in b2b_df.iterrows():
        for column, distance in row.items():
            distance_df.loc[len(distance_df.index)] = [f"{index} - {column}",distance]

    # Extract unique cities from City_Pair column
    city_pairs = distance_df['City_Pair'].str.split(' - ', expand=True)
    cities = pd.unique(city_pairs.values.ravel())
    
    # Initialize an empty distance matrix with cities as both row and column indices
    distance_matrix = pd.DataFrame(np.inf, index=cities, columns=cities)

    # Populate the matrix with distances
    for _, row in distance_df.iterrows():
        city1, city2 = row['City_Pair'].split(' - ')
        distance = row['Distance']
        # Set the distance for both [city1, city2] and [city2, city1] as the matrix is symmetric
        distance_matrix.loc[city1, city2] = distance
        distance_matrix.loc[city2, city1] = distance
        
    distance_matrix.drop([""],axis=0,inplace=True)
    distance_matrix.drop([""],axis=1,inplace=True)

    city_options = distance_matrix.columns
    
    options = st.multiselect("Blacklist city",city_options)

    distance_matrix.drop(options,axis=0,inplace=True)
    distance_matrix.drop(options,axis=1,inplace=True)

    # Fill diagonal with zeros, as distance from a city to itself is zero
    np.fill_diagonal(distance_matrix.values, 0)
    
    # Apply color gradient from green (low) to red (high) using 'RdYlGn'
    styled_matrix = distance_matrix.style.background_gradient(cmap="RdYlGn_r", vmin=0,vmax=2000, axis=1)

    # Show the resulting distance matrix
    st.dataframe(styled_matrix,use_container_width=True)

st.set_page_config(
    page_title="Distance Matrix",
    page_icon="🚚",
)

st.sidebar.header("Distance Matrix")
st.sidebar.markdown("Visualize the distances between each pair of nodes")

st.header("Distance matrix")
distance_file = st.file_uploader("Retail Distance (.csv)", type="csv")
b2b_file = st.file_uploader("B2B distance (.csv)",type="csv")
if distance_file and b2b_file:
    distance_matrix(distance_file,b2b_file)
