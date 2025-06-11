# Importing required modules.
import streamlit as st
import random
# Module containing task outline for Group A.
import tasks_a
# Module containing task outline for Group B.
import tasks_b

################################### Global Variables ################################

# Generating and storing ID number.
if "ID" not in st.session_state:
    st.session_state["ID"] = random.randint(1,1000000)

# Storing submitted ID number.
if "number" not in st.session_state:
    st.session_state.number = None

# Tracking ID form has been submitted successfully.
if "submitted" not in st.session_state:
    st.session_state.submitted = False

############################### Welcome Introduction #################################

st.title("Welcome to Stage 2 of this study!")

# Introduction to Stage 2 of study.
st.write("welcome paragraph quick run through what to expect. point towards ID generator. Make note of ID number for final survey.")

# ID generator.
st.subheader(f"Your personal ID: {st.session_state.ID}")

# Form to record participants ID number.
with st.form("ID_form"):
    # Logging ID number.
    ID_input = st.text_area("Enter Personal ID Here")
    # Generating submit button.
    submitted = st.form_submit_button(label="Submit")

    if submitted:
        # Validating input is a number.
        if ID_input.strip().isdigit():
            # Storing valid ID.
            st.session_state['number'] = ID_input
            # Marking form as submitted.
            st.session_state['submitted'] = True
        # Error for invalid input.
        else:
            st.error("Please enter the generated **numeric** ID")
            
##################################### Redirecting to Tasks ############################

# Determining group and redirecting to appropriate tasks.
if st.session_state['submitted']:
    number = st.session_state['number']
    st.write(f"Submitted number: {int(number)}")

    # Even ID numbers go to Group A.
    if int(number) % 2 == 0:
        # Only one option to prevent confusion.
        page = st.selectbox("You are", ["Group A"])
        # Launching Group A tasks.
        if page == "Group A":
            tasks_a.main()
    # Odd ID numbers go to Group B.
    else:
        page = st.selectbox("You are", ["Group B"])
        # Launching Group B tasks.
        if page == "Group B":
            tasks_b.main()

    