import streamlit as st
import math

st.set_page_config(
    page_title="Safety stock",
    page_icon="📦",
)
st.sidebar.header("Safety stock calculator")
st.sidebar.markdown("")

Z = st.number_input("Z",value=1.96)
average_lead_time = st.number_input("Average lead time",value=2)
lead_time_std_dev = st.number_input("Lead time standard deviation",value=1)
average_sale = st.number_input("Adverage sale per day",value=1000)
std_dev_demand = st.number_input("sales per day Standard deviation",value=100)

# คำนวณตามสูตร
result = Z * math.sqrt((average_lead_time * (std_dev_demand ** 2)) + (average_sale * (lead_time_std_dev ** 2)))

st.markdown(f'''
            ***
            Safety stock formula : {round(result)}
''')