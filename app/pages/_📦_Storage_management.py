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
    r, g, b = color  # ค่า RGB ของสีต้นฉบับ
    # ผสมกับสีขาว (1,1,1) เพื่อให้สีจางลง
    faded_color = [(1 - alpha) * r + alpha, (1 - alpha) * g + alpha, (1 - alpha) * b + alpha]
    return matplotlib.colors.to_hex(faded_color)

def highlight_by_dynamic_city(row):
    city = row.name[0]  # ดึงชื่อเมืองจาก MultiIndex
    color = city_colors.get(city, "#ffffff")  # ใช้สีที่จัดไว้ตามลำดับ
    faded_color = fade_color(color, alpha=0.3)  # ทำให้สีจางลงด้วย alpha
    return [f'background-color: {faded_color}'] * len(row)

def highlight_by_dynamic_product(row):
    product = row.name
    color = product_colors.get(product, "#ffffff")
    faded_color = fade_color(color, alpha=0.3)
    return [f'background-color: {faded_color}'] * len(row)

b2c_file = st.file_uploader("B2C forecast",type="csv")
if b2c_file :
    b2c_df = pd.read_csv(b2c_file)
    # ลบคอลัมน์ 'Category' ออกเพราะไม่ได้ใช้ในการคำนวณ
    b2c_df = b2c_df.drop(columns=["Category"])

    # แยกชื่อคอลัมน์เพื่อสร้าง MultiIndex โดยแบ่งเป็น 'City' และ 'Product'
    new_columns = pd.MultiIndex.from_tuples(
        [col.split('-', 1) for col in b2c_df.columns], names=["City", "Product"]
    )
    b2c_df.columns = new_columns
    city_options = new_columns.get_level_values(0).drop_duplicates(keep='first')
    options = st.multiselect("please select city",city_options,default=city_options[0])
    try:
        result = b2c_df[options].agg(['mean','std'])
        result_t = result.T
        result_t=  result_t.astype({'mean':'int64','std':'int64'})
        
        Z = st.number_input("Z-score (e.g., 1.65 for 95% confidence level)", value=1.65)
        
        # เตรียม dictionary เพื่อเก็บค่า Safety Stock ที่คำนวณ
        safety_stock_dict = {}

        for i in options:  # loop ทุก (City, Product) ใน index ของ result_t
            st.subheader(f"Settings for {i}")  

            avg_lead_time = st.number_input(f"Average lead time (days) for {i}", value=2, key=f"average_lead_time_{i}",min_value=1)
            lead_time_std_dev = st.number_input(f"Lead time standard deviation for {i}", value=1, key=f"lead_time_std_dev_{i}",min_value=1)
            expect_player = st.number_input(f"Expect player in market for {i}",value=1, key=f"expect_player_{i}",min_value=1)

            for j in new_columns.get_level_values(1).drop_duplicates(keep="first"): # loop
                avg_sale = result_t.loc[(i, j), 'mean']
                std_dev_demand = result_t.loc[(i, j), 'std']
                
                safety_stock = Z * math.sqrt(
                    (avg_lead_time * (std_dev_demand ** 2)) + (((avg_sale / expect_player) * lead_time_std_dev) ** 2)
                )
                safety_stock_dict[(i, j)] = int(safety_stock)

        result_t['Safety Stock'] = result_t.index.map(safety_stock_dict.get)
        
        # สร้างชุดสีโดยใช้ seaborn หรือชุดสีอื่น ๆ
        colors = sns.color_palette("muted", len(new_columns.get_level_values(0).unique()))
        city_colors = {city: colors[i] for i, city in enumerate(new_columns.get_level_values(0).drop_duplicates(keep='first'))}
        
        
        result_t = result_t.style.apply(highlight_by_dynamic_city, axis=1)
        st.dataframe(result_t,
            use_container_width= True)

    except Exception as e:
        st.error("Error : Please select at least one city.")
        print(e)
    
    

b2b_file = st.file_uploader("B2B forecast",type="csv")
if b2b_file:
    b2b_df = pd.read_csv(b2b_file)
    b2b_df.drop(columns=["Day"],inplace=True)
    result = b2b_df.agg(['mean','std'])
    result_t = result.T
    result_t = result_t.astype({'mean':'int64','std':'int64'})
    Z = st.number_input("Z-score (e.g., 1.65 for 95% confidence level)", value=1.65)
    safety_stock_dict = {}
    for i in result_t.index.unique():
        st.subheader(f"Settings for {i}")  
        
        avg_lead_time = st.number_input(f"Average lead time (days) for {i}", value=2, min_value=1)
        lead_time_std_dev = st.number_input(f"Lead time standard deviation for {i}", value=1,min_value=1)        
        avg_sale = result_t.loc[(i), 'mean']
        std_dev_demand = result_t.loc[(i), 'std']
        
        safety_stock = Z * math.sqrt(
            (avg_lead_time * (std_dev_demand ** 2)) + (((avg_sale) * lead_time_std_dev) ** 2)
        )
        safety_stock_dict[(i)] = int(safety_stock)

    result_t['Safety Stock'] = result_t.index.map(safety_stock_dict.get)

    colors = sns.color_palette("muted", len(result_t.index.unique()))
    product_colors = {product: colors[i] for i, product in enumerate(result_t.index.unique())}
    
    result_t = result_t.style.apply(highlight_by_dynamic_product, axis=1)

    st.dataframe(result_t,use_container_width=True)
