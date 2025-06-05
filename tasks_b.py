import streamlit as st
import numpy as np 
import matplotlib.pyplot as plt

def main():
    st.title("Coding Tasks")

    
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Introduction", "Task 1", "Task 2", "Debrief"])

    with tab1:
        st.subheader("Introduction")
        st.write("Introduce participants to this stage of the study. Explain conditions of task: 1. The use of any external tools is strictly prohibited / Use AI as you please. 2. You will be timed but complete the task like you normally would. 3. Task 2 will become available once task 1 is complete, take a break between tasks if you wish.")

    with tab2:
        st.subheader("Python Task 1")
        st.write("Introduce participants to task 1 conditions")
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
            with tab3:
                st.subheader("Python Task 2")
                st.write("Introduce participants to task 2 conditions")
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
                    with tab4:
                        st.subheader("Participant Debrief")
                        st.write("Debrief statement: Thank you for participating in this stage of the study. Please follow the link to the final survey, this will only take 5-10 minutes of your time. Please copy your ID number and save it for the start of the survey. [link to final survey].")
        

if __name__ == "__main__":
    main()
