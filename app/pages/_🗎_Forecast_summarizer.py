import matplotlib
import streamlit as st
import pandas as pd 
import seaborn as sns 

def fade_color(color, alpha=0.3):
    r, g, b = color  # ค่า RGB ของสีต้นฉบับ
    # ผสมกับสีขาว (1,1,1) เพื่อให้สีจางลง
    faded_color = [(1 - alpha) * r + alpha, (1 - alpha) * g + alpha, (1 - alpha) * b + alpha]
    return matplotlib.colors.to_hex(faded_color)

def b2c_handle(b2c_df):    
    def highlight_by_dynamic_city(row):
        city = row.name[0]  # ดึงชื่อเมืองจาก MultiIndex
        color = city_colors.get(city, "#ffffff")  # ใช้สีที่จัดไว้ตามลำดับ
        faded_color = fade_color(color, alpha=0.3)  # ทำให้สีจางลงด้วย alpha
        return [f'background-color: {faded_color}'] * len(row)


    b2c_df = pd.read_csv(b2c_file)
    try:
        b2c_df = b2c_df.drop(columns=["Category"])
    except Exception as e:
        st.error("Error : Data is wrong format.")
        print(e)
        return
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

        # สร้างชุดสีโดยใช้ seaborn หรือชุดสีอื่น ๆ
        colors = sns.color_palette("muted", len(new_columns.get_level_values(0).unique()))
        city_colors = {city: colors[i] for i, city in enumerate(new_columns.get_level_values(0).drop_duplicates(keep='first'))}
        
        
        result_t = result_t.style.apply(highlight_by_dynamic_city, axis=1)
        st.dataframe(result_t,
                use_container_width= True)
    except Exception as e:
        print(e)
        st.error("Error : Please select at least one city.")
        return 
def b2b_handle(b2b_df):
    
    def highlight_by_dynamic_product(row):
        product = row.name
        color = product_colors.get(product, "#ffffff")
        faded_color = fade_color(color, alpha=0.3)
        return [f'background-color: {faded_color}'] * len(row)


    b2b_df = pd.read_csv(b2b_file)
    b2b_df.drop(columns=["Day"],inplace=True)
    result = b2b_df.agg(['mean','max','min','std'])
    result_t = result.T
    result_t = result_t.astype({'mean':'int64','std':'int64'})
    
    # สร้างชุดสีโดยใช้ seaborn หรือชุดสีอื่น ๆ
    colors = sns.color_palette("muted", len(result_t.index.unique()))
    product_colors = {product: colors[i] for i, product in enumerate(result_t.index.unique())}
    
    result_t = result_t.style.apply(highlight_by_dynamic_product, axis=1)

    st.dataframe(result_t,use_container_width=True)

st.set_page_config(
    page_title="Forecasting summarizer",
    page_icon="🗎",
)
st.sidebar.header("Forecasting summarizer")
st.sidebar.markdown("ช่วยในการสรุปผลการทำนายความต้องการของลูกค้า")


b2c_file = st.file_uploader("B2C forecast",type="csv")
if b2c_file:
    b2c_handle(b2c_file)

b2b_file = st.file_uploader("B2B forecast",type="csv")
if b2c_file:
    b2b_handle(b2b_file)