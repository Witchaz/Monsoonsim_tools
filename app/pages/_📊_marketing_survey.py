import streamlit as st
import pandas as pd
import numpy as np


def cal():
    if in1 == None or in1 == "" or isinstance(in1,str):
        st.error("Please enter a valid number for Group 1 max age.")
        return
    elif in2 == None or in2 == "" or isinstance(in1,str):
        st.error("Please enter a valid number for Group 3 min age.")
        return
    elif file == None:
        st.error("Please upload a marketing survey (.csv) file.")
        return
    

    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    

    df['Age Group'] = pd.cut(df['Age'], bins=[0, 30, 60, float('inf')], labels=['30 and below', '30-60', 'Above 60'])
    df = df.groupby(['Age Group','Product Preference'])['Media Preference'].value_counts().unstack(fill_value=0)
    df.reset_index(inplace=True)
    df = df.style.background_gradient(cmap="RdPu", subset=['Media A', 'Media B', 'Media C'])

    st.dataframe(df,hide_index=True)

st.set_page_config(
    page_title="Main",
    page_icon="🤖",
)
st.sidebar.header("Marketing survey summarizer")
st.sidebar.markdown("เว็บที่จะช่วยสรุปข้อมูลใน Marketing survey ให้คุณ โดยในนี้จะใช้ระบบ 100 samples ถ้าใช้เป็นตัวอื่นค่าที่จะช่วยไฮไลต์อาจจะเพี้ยน")

in1 = st.number_input("Group 1 max age",value=25)
in2 = st.number_input("Group 3 min age",value=60)
file = st.file_uploader("Marketing survey (.csv)",type="csv")

if st.button("submit"):
    cal()

    