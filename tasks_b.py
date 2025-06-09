import streamlit as st
import numpy as np 
import matplotlib.pyplot as plt

def main():
    st.title("Coding Tasks")

    if "task1_complete" not in st.session_state:
        st.session_state.task1_complete = False
    if "task2_complete" not in st.session_state:
        st.session_state.task2_complete = False
    if "debrief_tab" not in st.session_state:
        st.session_state.debrief_tab = False
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Introduction", "Task 1", "Task 2", "Debrief"])

    with tab1:
        st.subheader("Introduction")
        st.write("""
        Introduce participants to this stage of the study. Explain conditions of task: 1. The use of any external tools is strictly prohibited / Use AI as you please. 2. You will be timed but complete the task like you normally would. 3. Task 2 will become available once task 1 is complete, take a break between tasks if you wish.
        """)

    with tab2:
        st.subheader("Python Task 1")

        if st.session_state.task2_complete:
            st.info("Thank you for completing Task 1 please take a short break and move onto Task 2. Remember the use of any external tools is **strictly prohibited** in Task 2.")
            st.warning("Task 1 is now locked because you've moved on to Task 2.")

        else:
            st.write("Introduce participants to task 1 conditions. Double click to submit.")
            st.subheader("Data")
            with st.expander("Count how many times the speed increases by more than 30 units compared to the previous reading."):
                st.write("""
            Use the box below to:
            
            Step 1. Read each line and extract time stamp and speed.
            
            Step 2. Compare each speed to the previous one. 
            
            Step 3. Count cases where the difference is strictly greater than 30.
            """)
              # Forms
            with st.form(key="myform1"):
                task1_answer = st.text_area("Enter Python Code Here")
                submit_button1 = st.form_submit_button(label="Submit")

            if submit_button1:
                st.session_state.task1_complete = True
           
    with tab3:
        st.subheader("Python Task 2")
       
        if not st.session_state.task1_complete:
            st.warning("Please complete Task 1 before proceeding to Task 2.")
        elif st.session_state.debrief_tab:
            st.info("Thank you for completing Task 2. You may now proceed to the debrief tab.")
            st.warning("Task 2 is now locked because you've moved on to the debrief.")
        else:
            st.session_state.task2_complete = True
            st.write("Introduce participants to task 2 conditions. Double click to submit.")
            st.subheader("Data")
            with st.expander("Find the longest continuous segment where speed strictly increases at each step. Then return the total time duration of that segment (in seconds)."):
                st.write("""
            Use the box below to:

            Step 1. Read each row.
            
            Step 2. Compare speeds.

            Step 3. Track how long a run of increasing speed values continue.

            Step 4. Refer to timestamps to work out durations.
            """)
                # Forms
            with st.form(key="myform2"):
                task2_answer = st.text_area("Enter Python Code Here")
                submit_button2 = st.form_submit_button(label="Submit")

            if submit_button2:
                st.session_state.debrief_tab = True
                
    with tab4:
        st.subheader("Participant Debrief")
        if not st.session_state.task2_complete:
            st.warning("Please complete Task 2 to view the debrief.")
        else:
            st.write("""
            Debrief statement: Thank you for participating in this stage of the study. Please follow the link to the final survey, this will only take 5-10 minutes of your time. Please copy your ID number and save it for the start of the survey. [link to final survey].
            """)
        

if __name__ == "__main__":
    main()
