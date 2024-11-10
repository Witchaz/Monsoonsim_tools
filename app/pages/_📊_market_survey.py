import matplotlib 
import streamlit as st
import pandas as pd
import numpy as np



def cal():
    if in1 == None or in1 == "" or isinstance(in1,str):
        st.error("Please enter a valid number for Junior max age.")
        return
    elif in2 == None or in2 == "" or isinstance(in1,str):
        st.error("Please enter a valid number for elder min age.")
        return
    elif file == None:
        st.error("Please upload a marketing survey (.csv) file.")
        return
    

    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    
    try:
        df['Age Group'] = pd.cut(df['Age'], bins=[0, in1, in2, float('inf')], labels=[f'{in1} and below', f'{in1}-{in2}', f'Above {in2}'])
    except Exception as e:
        st.error("Error : Data is wrong format.")
        print(e)
        return
    
    media_list = df['Media Preference'].unique()
    df = df.groupby(['Age Group','Product Preference'])['Media Preference'].value_counts().unstack(fill_value=0)
    df.reset_index(inplace=True)
    df = df.style.background_gradient(cmap="RdPu", subset=media_list)

    st.dataframe(df,hide_index=True)

st.set_page_config(
    page_title="Marketing survey summarizer",
    page_icon="📊",
)
st.sidebar.header("Marketing survey summarizer")
st.sidebar.markdown("เว็บที่จะช่วยสรุปข้อมูลใน Marketing survey ให้คุณ โดยในนี้จะใช้ระบบ 100 samples ถ้าใช้เป็นตัวอื่นค่าที่จะช่วยไฮไลต์อาจจะเพี้ยน")

st.header("Market survey")

in1 = st.number_input("อายุสูงสุดของกลุ่มลูกค้าเด็ก",value=25,min_value=1)
in2 = st.number_input("อายุต่ำสุดของกลุ่มลูกค้าผู้สูงอายุ",value=60,min_value=in1+1)
file = st.file_uploader("Market Survey (.csv)",type="csv")

if st.button("submit"):
    cal()

    