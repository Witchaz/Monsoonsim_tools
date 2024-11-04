import streamlit as st
import pandas as pd 
st.set_page_config(
    page_title="Forecasting summarizer",
    page_icon="📊",
)
st.sidebar.header("Forecasting summarizer")
st.sidebar.markdown("ช่วยในการสรุปผลการทำนายความต้องการของลูกค้า")



b2c_file = st.file_uploader("B2C forecast")
if b2c_file :
    df = pd.read_csv(b2c_file)
    # ลบคอลัมน์ 'Category' ออกเพราะไม่ได้ใช้ในการคำนวณ
    df = df.drop(columns=["Category"])

    # แยกชื่อคอลัมน์เพื่อสร้าง MultiIndex โดยแบ่งเป็น 'City' และ 'Product'
    new_columns = pd.MultiIndex.from_tuples(
        [col.split('-', 1) for col in df.columns], names=["City", "Product"]
    )
    df.columns = new_columns
    city_options = new_columns.get_level_values(0).drop_duplicates(keep='first')
    options = st.multiselect("please select city",city_options,default=city_options[0])
    try:
        result = df[options].agg(['mean', 'max', 'min'])
        st.dataframe(result.T,
                use_container_width= True,
                column_config={})
    except:
        st.error("Error : Please select at least one city.")