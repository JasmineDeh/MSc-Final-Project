# Importing required modules.
import streamlit as st
import random
# Module containing task outline for Group A.
import tasks_a
# Module containing task outline for Group B.
import tasks_b

################################### Global Variables ################################

# Assigning and storing participant number.
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, 1000000)

number = st.session_state.number

############################### Welcome Introduction #################################

st.title("Welcome to Stage 2 of this study!")

# Introduction to Stage 2 of study.
st.write("welcome paragraph quick run through what to expect. point towards ID generator. Make note of ID number for final survey.")


# Form to record participants ID number.
with st.form("ID_form"):
    # Logging ID number.
    ID_input = st.text_area("Enter Memorable Word Here")
    # Generating submit button.
    submitted = st.form_submit_button(label="Submit")

    if submitted:
        # Redirecting to tasks: even numbers = Group A, odd numbers = Group B.
        if number % 2 == 0:
            st.success("You have been assigned to **Group A**.")
            tasks_a.main()
        else:
            st.success("You have been assigned to **Group B**.")
            tasks_b.main()
    