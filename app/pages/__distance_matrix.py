import matplotlib
import pandas as pd
import streamlit as st
import numpy as np

def distance_matrix(distance_file):
    df = pd.read_csv(distance_file)    
    df.columns = ['City_Pair', 'Distance']

    # Extract unique cities from City_Pair column
    city_pairs = df['City_Pair'].str.split(' - ', expand=True)
    cities = pd.unique(city_pairs.values.ravel())

    # Initialize an empty distance matrix with cities as both row and column indices
    distance_matrix = pd.DataFrame(np.inf, index=cities, columns=cities)

    # Populate the matrix with distances
    for _, row in df.iterrows():
        city1, city2 = row['City_Pair'].split(' - ')
        distance = row['Distance']
        # Set the distance for both [city1, city2] and [city2, city1] as the matrix is symmetric
        distance_matrix.loc[city1, city2] = distance
        distance_matrix.loc[city2, city1] = distance

    # Fill diagonal with zeros, as distance from a city to itself is zero
    np.fill_diagonal(distance_matrix.values, 0)
    distance_matrix = distance_matrix.iloc[0:-1,0:-1]
    # Apply color gradient from green (low) to red (high) using 'RdYlGn'
    styled_matrix = distance_matrix.style.background_gradient(cmap="RdYlGn_r", vmin=0,vmax=2000, axis=1)

    # Show the resulting distance matrix
    st.dataframe(styled_matrix,use_container_width=True)

st.set_page_config(
    page_title="Distance Matrix",
    page_icon="📦",
)

st.sidebar.header("Distance Matrix")
st.sidebar.markdown("Visualize the distances between each pair of nodes")

distance_file = st.file_uploader("Distance (.csv)", type="csv")
if distance_file:
    distance_matrix(distance_file)
