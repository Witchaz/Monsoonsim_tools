import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="Safety stock",
    page_icon="📦",
)



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
        safety_stock_values = []  # เก็บค่าที่คำนวณได้สำหรับแต่ละเมืองและผลิตภัณฑ์

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
    st.dataframe(result_t,use_container_width=True)

    avg_lead_time = st.number_input(f"Average lead time (days) for {i}", value=2, key=f"average_lead_time_{i}",min_value=1)
    lead_time_std_dev = st.number_input(f"Lead time standard deviation for {i}", value=1, key=f"lead_time_std_dev_{i}",min_value=1)