import streamlit as st
import math

st.set_page_config(
    page_title="Space calcutator",
    page_icon="📏",
)
st.sidebar.title("Space calcutator")
st.sidebar.markdown("ช่วยคำนวณพื้นที่สำหรับ จำนวนของที่เราต้องการ")

if "products" not in st.session_state:
    st.session_state.products = []
def add_input():
    new_key = f"product_{len(st.session_state.products) + 1}"
    st.session_state.products.append({"key": new_key})

def remove_input(index):
    if 0 <= index < len(st.session_state.products):
        del st.session_state.products[index]  # Remove the entry at the specified index
        st.rerun()

st.title("Space calculator")

if st.button("Add Input"):
    add_input()

for index, item in enumerate(st.session_state.products):
    key = item["key"]
    st.subheader(f"Product {key.split("_")[1]}")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.session_state.products[index]["size"] = st.number_input(label="Size",value=0.00500, key=f"{key}_size",format="%0.5f",min_value=0.0)
    with col2:
        st.session_state.products[index]["volumn"] = st.number_input(label="Volume",value=1000, key=f"{key}_volumn",step=100,min_value=0)
    with col3:
        st.session_state.products[index]["area"] =  st.text_input(label="area",value = f"{st.session_state[f"{key}_size"] * st.session_state[f"{key}_volumn"]:.2f}",disabled=True,key = f"{key}_area")

if len(st.session_state.products) > 0:
    if st.button(f"Remove Product {key.split("_")[1]}", key=f"remove_{key}"):
        remove_input(len(st.session_state.products) - 1)

total_area = 0
total_inventory = 0 
for i in st.session_state.products:
    total_inventory += (i["volumn"])
    total_area += float(i["area"])

st.write(f"Total item in inventory: {total_inventory:.2f}")
st.write(f"Total area required : {total_area:.2f}")