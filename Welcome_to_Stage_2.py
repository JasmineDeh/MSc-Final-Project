# Importing required modules.
import streamlit as st
import random
# Module containing task outline for Group A.
import tasks_a
# Module containing task outline for Group B.
import tasks_b

################################### Variables ################################

# Assigning and storing participant number.
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, 1000000)

number = st.session_state.number

############################### Welcome Introduction #################################

st.title("Welcome to Stage 2 of this study!")

# Introduction to Stage 2 of study.
st.write("""
Thank you for continuing with the study!

In this stage, you'll be automatically assigned to one of two task groups. Please work through the activity carefully and follow any on-screen instructions.

Once you've completed the tasks, you'll be directed to a short follow-up survey which will only take 5-10 minutes of your time.

Please enter your memorable word, which you chose in the first survey, into the box below. Your memorable word will also be required for the final survey.

Once you've submitted your memorable word you will be assigned to a task group.

""")

# Form to record participants ID number.
with st.form("ID_form"):
    # Logging ID number.
    ID_input = st.text_area("Enter Memorable Word Here")
    # Generating submit button.
    submitted = st.form_submit_button(label="Submit")

    if submitted:
        st.session_state.ID_input = ID_input
        st.session_state.ID_submitted = True
        st.rerun() 

# Redirecting to tasks: even numbers = Group A, odd numbers = Group B.
if st.session_state.get("ID_submitted", False):
    if number % 2 == 0:
        st.success("You have been assigned to **Group A**.")
        tasks_a.main()
    else:
        st.success("You have been assigned to **Group B**.")
        tasks_b.main()
    