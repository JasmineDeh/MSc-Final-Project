import streamlit as st
import random
import tasks_a
import tasks_b

st.set_page_config(
    page_title="ID Generator",
)

st.title("Welcome to Stage 2 of this study!")
st.write("welcome paragraph quick run through what to expect. point towards ID generator. Make note of ID number for final survey.")


if "ID" not in st.session_state:
    st.session_state["ID"] = random.randint(1,1000000)

if "number" not in st.session_state:
    st.session_state.number = None
    
if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.subheader(f"Your personal ID: {st.session_state.ID}")

with st.form("ID_form"):
    ID_input = st.text_area("Enter Personal ID Here")
    submitted = st.form_submit_button(label="Submit")
    
    if submitted:
        if ID_input.strip().isdigit():
            st.session_state['number'] = ID_input
            st.session_state['submitted'] = True
        else:
            st.error("Please enter the generated **numeric** ID")
    
if st.session_state['submitted']:
    number = st.session_state['number']
    st.write(f"Submitted number: {int(number)}")
    
    if int(number) % 2 == 0:
        page = st.selectbox("You are", ["Group A"])
        if page == "Group A":
            tasks_a.main()
    else:
        page = st.selectbox("You are", ["Group B"])
        if page == "Group B":
            tasks_b.main()

    