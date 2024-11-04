import streamlit as st


st.set_page_config(
    page_title="Home",
    page_icon="🤖",
)
col1,col2,col3 = st.columns(3)
with col2 :
    st.image("./app/images/Salefork.png","Salefork logo",width=300)

st.markdown('''
            # เราจะช่วยอะไรคุณ?
            ***
            1) สรุป Marketing survey 📊
            2) ช่วยคำนวณหา Safety stock และ Reorder point 📦
            3) ช่วยสรุป Forecast ทั้งฝั่ง B2B และ B2C 🗎
            4) ยังทำเสร็จอ่ะ 🥹

            ''')
