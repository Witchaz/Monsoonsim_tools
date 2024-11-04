import matplotlib
import streamlit as st
import pandas as pd
import seaborn as sns
import math

st.set_page_config(
    page_title="Safety stock",
    page_icon="📦",
)

def fade_color(color, alpha=0.3):
    r, g, b = color
    faded_color = [(1 - alpha) * r + alpha, (1 - alpha) * g + alpha, (1 - alpha) * b + alpha]
    return matplotlib.colors.to_hex(faded_color)

# ฟังก์ชันสำหรับการ highlight ของ B2C
def b2c_highlight_by_city(row):
    city = row.name[0]
    color = b2c_city_colors.get(city, "#ffffff")
    faded_color = fade_color(color, alpha=0.3)
    return [f'background-color: {faded_color}'] * len(row)

# ฟังก์ชันสำหรับการ highlight ของ B2B
def b2b_highlight_by_product(row):
    product = row.name
    color = b2b_product_colors.get(product, "#ffffff")
    faded_color = fade_color(color, alpha=0.3)
    return [f'background-color: {faded_color}'] * len(row)

# B2C Processing
b2c_file = st.file_uploader("B2C forecast", type="csv")
if b2c_file:
    b2c_df = pd.read_csv(b2c_file)
    b2c_df = b2c_df.drop(columns=["Category"])
    new_columns = pd.MultiIndex.from_tuples(
        [col.split('-', 1) for col in b2c_df.columns], names=["City", "Product"]
    )
    b2c_df.columns = new_columns
    b2c_city_options = new_columns.get_level_values(0).drop_duplicates(keep='first')
    b2c_options = st.multiselect("Please select city", b2c_city_options, default=b2c_city_options[0])

    try:
        b2c_result = b2c_df[b2c_options].agg(['mean', 'std'])
        b2c_result_t = b2c_result.T
        b2c_result_t = b2c_result_t.astype({'mean': 'int64', 'std': 'int64'})
        
        b2c_Z = st.number_input("B2C Z-score (e.g., 1.65 for 95% confidence level)", value=1.65)
        b2c_safety_stock_dict = {}
        b2c_reorder_point_dict = {}

        for i in b2c_options:
            st.subheader(f"Settings for {i}")
            avg_lead_time = st.number_input(f"Average lead time (days) for {i}", value=2, key=f"b2c_average_lead_time_{i}", min_value=1)
            lead_time_std_dev = st.number_input(f"Lead time standard deviation for {i}", value=1, key=f"b2c_lead_time_std_dev_{i}", min_value=1)
            expect_player = st.number_input(f"Expect player in market for {i}", value=1, key=f"b2c_expect_player_{i}", min_value=1)

            for j in new_columns.get_level_values(1).drop_duplicates(keep="first"):
                avg_sale = b2c_result_t.loc[(i, j), 'mean']
                std_dev_demand = b2c_result_t.loc[(i, j), 'std']
                
                safety_stock = b2c_Z * math.sqrt(
                    (avg_lead_time * (std_dev_demand ** 2)) + (((avg_sale / expect_player) * lead_time_std_dev) ** 2)
                )
                b2c_safety_stock_dict[(i, j)] = int(safety_stock)
                b2c_reorder_point_dict[(i, j)] = int(safety_stock) + (avg_sale * avg_lead_time)

        b2c_result_t['Safety Stock'] = b2c_result_t.index.map(b2c_safety_stock_dict.get)
        b2c_result_t['Reorder Point'] = b2c_result_t.index.map(b2c_reorder_point_dict.get)
        
        b2c_colors = sns.color_palette("muted", len(new_columns.get_level_values(0).unique()))
        b2c_city_colors = {city: b2c_colors[i] for i, city in enumerate(new_columns.get_level_values(0).drop_duplicates(keep='first'))}
        
        b2c_result_t = b2c_result_t.style.apply(b2c_highlight_by_city, axis=1)
        st.dataframe(b2c_result_t, use_container_width=True)

    except Exception as e:
        st.error("Error: Please select at least one city.")
        print(e)

# B2B Processing
b2b_file = st.file_uploader("B2B forecast", type="csv")
if b2b_file:
    b2b_df = pd.read_csv(b2b_file)
    b2b_df.drop(columns=["Day"], inplace=True)
    b2b_result = b2b_df.agg(['mean', 'std'])
    b2b_result_t = b2b_result.T
    b2b_result_t = b2b_result_t.astype({'mean': 'int64', 'std': 'int64'})
    
    b2b_Z = st.number_input("B2B Z-score (e.g., 1.65 for 95% confidence level)", value=1.65)
    b2b_safety_stock_dict = {}
    b2b_reorder_point_dict = {}

    avg_lead_time = st.number_input(f"Average lead time (days) for warehouse", value=2, min_value=1)
    lead_time_std_dev = st.number_input(f"Lead time standard deviation for warehouse", value=1, min_value=1)
    
    for i in b2b_result_t.index.unique():
        avg_sale = b2b_result_t.loc[i, 'mean']
        std_dev_demand = b2b_result_t.loc[i, 'std']
        
        safety_stock = b2b_Z * math.sqrt(
            (avg_lead_time * (std_dev_demand ** 2)) + (((avg_sale) * lead_time_std_dev) ** 2)
        )
        b2b_safety_stock_dict[i] = int(safety_stock)
        b2b_reorder_point_dict[i] = int(safety_stock) + (avg_sale * avg_lead_time)

    b2b_result_t['Safety Stock'] = b2b_result_t.index.map(b2b_safety_stock_dict.get)
    b2b_result_t['Reorder point'] = b2b_result_t.index.map(b2b_reorder_point_dict.get)

    b2b_colors = sns.color_palette("muted", len(b2b_result_t.index.unique()))
    b2b_product_colors = {product: b2b_colors[i] for i, product in enumerate(b2b_result_t.index.unique())}
    
    b2b_result_t = b2b_result_t.style.apply(b2b_highlight_by_product, axis=1)
    st.dataframe(b2b_result_t, use_container_width=True)
