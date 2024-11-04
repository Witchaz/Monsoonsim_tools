import streamlit as st
import pandas as pd 
import statistics 
st.set_page_config(
    page_title="Forecasting summarizer",
    page_icon="📊",
)
st.sidebar.header("Forecasting summarizer")
st.sidebar.markdown("ช่วยในการสรุปผลการทำนายความต้องการของลูกค้า")



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
        result = b2c_df[options].agg(['mean', 'max', 'min','std'])
        result_t = result.T
        result_t=  result_t.astype({'mean':'int64','std':'int64'})
        st.dataframe(result_t,
                use_container_width= True)
    except:
        st.error("Error : Please select at least one city.")

b2b_file = st.file_uploader("B2B forecast",type="csv")
if b2b_file:
    b2b_df = pd.read_csv(b2b_file)
    b2b_df.drop(columns=["Day"],inplace=True)
    result = b2b_df.agg(['mean','max','min','std'])
    result_t = result.T
    result_t = result_t.astype({'mean':'int64','std':'int64'})
    st.dataframe(result_t,use_container_width=True)