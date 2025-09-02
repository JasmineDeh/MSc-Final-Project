"""
Stage 2 Streamlit App for Generative AI Study

This script implements the interactive Stage 2 task interface for participants
in the generative AI cognitive impact study. Participants are automatically
assigned to one of two task groups (A or B) and work through tasks based on
their assigned group.

Functionality:

1. Session Initialisation:
   - Assigns a unique participant number if not already present in the session state.
   - Stores participant information for the session.

2. Welcome Introduction:
   - Displays instructions and context for Stage 2.
   - Guides participants to enter their memorable word from Stage 1.

3. Participant Identification:
   - Collects the participant's memorable word through a Streamlit form.
   - Stores submission state to control task assignment.

4. Task Group Assignment:
   - Participants with even session numbers are assigned to Group A.
   - Participants with odd session numbers are assigned to Group B.
   - Calls the corresponding task module (`tasks_a` or `tasks_b`) to start the tasks.



Run the app via terminal:

  streamlit run Welcome_to_Stage_2.py

"""

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
    