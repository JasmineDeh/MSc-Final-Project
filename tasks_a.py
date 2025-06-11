# Importing required modules.
import streamlit as st
import numpy as np 
import pandas as pd
import time

# Intialising main function.

def main():
    st.title("Coding Tasks")

##################################### Global Variables #################################

    # Generating DataFrame required for tasks.
    df = pd.DataFrame(
        { 
            "Time Stamp": [0, 1, 2, 3, 4, 5, 6],
            "Speed": [20, 25, 60, 50, 55, 90, 95]
        }
    )
    df.set_index("Time Stamp", inplace=True)

    # Initialise Tab 2 (Task 1) session state variables for tracking and timing.
    if "task1_start_time" not in st.session_state:
        st.session_state.task1_start_time = None
    if "task1_end_time" not in st.session_state:
        st.session_state.task1_end_time = None
    if "task1_duration" not in st.session_state:
        st.session_state.task1_duration = None
    if "task1_started" not in st.session_state:
        st.session_state.task1_started = False
    if "task1_complete" not in st.session_state:
        st.session_state.task1_complete = False

    # Initialise Tab 3 (Task 2) session state variables for tracking and timing.
    if "task2_start_time" not in st.session_state:
        st.session_state.task2_start_time = None
    if "task2_end_time" not in st.session_state:
        st.session_state.task2_end_time = None
    if "task2_duration" not in st.session_state:
        st.session_state.task2_duration = None
    if "task2_started" not in st.session_state:
        st.session_state.task2_started = False 
    if "task2_complete" not in st.session_state:
        st.session_state.task2_complete = False

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Introduction", "Task 1", "Task 2", "Debrief"])
    
################################## Introduction #######################################
    
    with tab1:
        st.subheader("Introduction")
        # Tasks introductory information shown to participants.
        st.write("""
        Introduce participants to this stage of the study. Explain conditions of task: 1. The use of any external tools is strictly prohibited / Use AI as you please. 2. You will be timed but complete the task like you normally would. 3. Task 2 will become available once task 1 is complete, take a break between tasks if you wish. 4. once you click on task 1 tab the timer will start, it will not stop until submit is hit, the same applies for task 2, please still take as long as you need to in each task.
        """)

#################################### Task 1 ##############################################
    
    with tab2:
        st.subheader("Python Task 1")

        # Information shown to participant once Task 1 is submitted.
        if st.session_state.task1_complete:
            
            # Show participants result and whether it was correct or not.
            if "task1_user_result" in st.session_state:
                if st.session_state.task1_success:
                    st.success(f"Your answer: {st.session_state.task1_user_result} (Correct!).")
                else:
                    st.error(f"Your answer: {st.session_state.task1_user_result}. Correct answer: {st.session_state.task1_correct_result}.")

            # Other information shown to participants regarding tasks.
            st.info(f"Thank you for completing Task 1 (time taken: {st.session_state.task1_duration:.2f} seconds), please take a short break and move onto Task 2. Remember the use of any external tools is **strictly prohibited** in Task 2.")
            st.warning("Task 1 is now locked, please move on to Task 2.")
            
        # Information shown to participants once Task 1 is started.
        elif st.session_state.task1_started:
            
            # Logging Task 1 start time.
            if st.session_state.task1_start_time is None:
                st.session_state.task1_start_time = time.time()
                
            # Displaying data required for tasks.
            st.subheader("Time Stamped Speed Data:")
            st.dataframe(df)

            # Task 1 information.
            st.subheader("Count how many times the speed increases by more than 30 units compared to the previous reading.")
            with st.expander("Click here for more info."):
                st.write("""
            Use the box below to:
            
            Step 1. Read each line and extract time stamp and speed.
            
            Step 2. Compare each speed to the previous one. 
            
            Step 3. Count cases where the difference is strictly greater than 30.
            """)
              
            # Form to record participants answer.
            with st.form(key="a_task_1_form"):
                # Logging Task 1 answer.
                task1_answer = st.text_area("Enter Python Code Here")
                # Generating submit button.
                submit_button1 = st.form_submit_button(label="Submit")

            st.write("You only get **ONE ATTEMPT** at submitting your code. Please read through it carefully.")
            
            if submit_button1:
                # Logging Task 1 end time.
                st.session_state.task1_end_time = time.time()
                # Calculating Task 1 duration.
                st.session_state.task1_duration = (
                    st.session_state.task1_end_time - st.session_state.task1_start_time
                )

                # Calculating correct answer for Task 1.
                task1_correct = 0
                speeds = df["Speed"].tolist()
                for i in range(1, len(speeds)):
                    if speeds[i] - speeds[i - 1] > 30:
                        task1_correct += 1

                # Running participants code and extracting results.
                try:
                    # Isolating participants result.
                    local_vars = {}
                    exec(task1_answer, {}, local_vars)
                    user_result = local_vars.get("result", None)

                    # Storing results in session state variables.
                    st.session_state.task1_user_result = user_result
                    st.session_state.task1_correct_result = task1_correct
                    st.session_state.task1_success = (user_result == task1_correct)
               
                # Catching any errors in the participants code.
                except Exception as e:
                    user_result = None
                    st.session_state.task1_user_result = f"Error: {e}"
                    st.session_state.task1_correct_result = task1_correct
                    st.session_state.task1_success = False
                    
                # Logging Task 1 as complete.
                st.session_state.task1_complete = True
                # Rerunning the code so that new information is shown to participants.
                st.experimental_rerun()

        # What participants see before having access to Task 1.
        else:
            # Information for participants regarding Task 1.
            st.write("Introduce participants to task 1 conditions. You only get 1 attempt at submitting code.")

            # Form to record participants understand Task 1 rules.
            with st.form(key="a_info_1_form"):
                info1_submit = st.form_submit_button(label="Start Task.")

            if info1_submit:
                # Logging Task 1 as started.
                st.session_state.task1_started = True
                # Rerunning the code so that participants have access to Task 1
                st.experimental_rerun()

########################################## Task 2 #############################################            
            
    with tab3:
        st.subheader("Python Task 2")

        # Information shown to participants if Task 1 is not complete.
        if not st.session_state.task1_complete:
            st.warning("Please complete Task 1 before proceeding to Task 2.")

        # Information shown to participants once Task 2 is submitted.
        if st.session_state.task2_complete:

            # Show participants result and whether it was correct or not.
            if "task2_user_result" in st.session_state:
                if st.session_state.task2_success:
                    st.success(f"Your answer: {st.session_state.task2_user_result} (Correct!).")
                else:
                    st.error(f"Your answer: {st.session_state.task2_user_result}. Correct answer: {st.session_state.task2_correct_result}.")
            
            # Other information shown to participants regarding tasks.
            st.info(f"Thank you for completing Task 2 (time taken: {st.session_state.task2_duration:.2f}). You may now proceed to the debrief tab.")
            st.warning("Task 2 is now locked, please move on to the debrief.")

        # Information shown to participants once Task 2 is started.
        elif st.session_state.task2_started:
            
            # Logging Task 2 start time.
            if st.session_state.task2_start_time is None:
                st.session_state.task2_start_time = time.time()
                
            # Displaying data required for tasks.
            st.subheader("Time Stamped Speed Data:")
            st.dataframe(df)

            # Task 2 information.
            st.subheader("Find the longest continuous segment where speed strictly increases at each step. Then return the total time duration of that segment (in seconds).")
            with st.expander("Click here for more info."):
                st.write("""
            Use the box below to:

            Step 1. Read each row.
            
            Step 2. Compare speeds.

            Step 3. Track how long a run of increasing speed values continue.

            Step 4. Refer to timestamps to work out durations.
            """)
                
            # Form to record participants answer.
            with st.form(key="a_task_2_form"):
                # Logging Task 2 answer.
                task2_answer = st.text_area("Enter Python Code Here")
                # Generating submit button.
                submit_button2 = st.form_submit_button(label="Submit")

            st.write("You only get **ONE ATTEMPT** at submitting your code. Please read through it carefully.")
            
            if submit_button2:
                # Logging Task 2 end time.
                st.session_state.task2_end_time = time.time()
                # Calculating Task 2 duration.
                st.session_state.task2_duration = (
                    st.session_state.task2_end_time - st.session_state.task2_start_time
                )

                # Calculating correct answer.
                speeds = df["Speed"].tolist()
                timestamps = df.index.tolist()
                max_duration = 0
                start = 0

                for i in range(1, len(speeds)):
                    if speeds[i] > speeds[i - 1]:
                        continue
                    else:
                        duration = timestamps[i - 1] - timestamps[start]
                        if duration > max_duration:
                            max_duration = duration
                        start = i
                # Final check after loop.
                duration = timestamps[-1] - timestamps[start]
                if duration > max_duration:
                    max_duration = duration

                try:
                    # Isolating participants results.
                    local_vars = {}
                    exec(task2_answer, {}, local_vars)
                    user_result = local_vars.get("result", None)

                    # Storing results in session state variables.
                    st.session_state.task2_user_result = user_result
                    st.session_state.task2_correct_result = max_duration
                    st.session_state.task2_success = (user_result == max_duration)

                # Catching any errors in the participants code.
                except Exception as e:
                    user_result = None
                    st.session_state.task2_user_result = f"Error: {e}"
                    st.session_state.task2_correct_result = max_duration
                    st.session_state.task2_success = False
                    
                # Logging Task 2 as complete.
                st.session_state.task2_complete = True
                # Rerunning the code so that new information is shown to participants.
                st.experimental_rerun()

        # What participants see before having acces to Task 2.
        if st.session_state.task1_complete and not st.session_state.task2_complete and not st.session_state.task2_started:
            
            # Information for participants regarding Task 2.
            st.write("Introduce participants to task 2 conditions.")
            
            # Form to record participants understand Task 2 rules.
            with st.form(key="a_info_2_form"):
                info2_submit = st.form_submit_button(label="Start Task.")

            if info2_submit:
                # Logging Task 2 as started.
                st.session_state.task2_started = True
                # Rerunning the code so that participants have access to Task 1
                st.experimental_rerun()
            
############################################# Debrief ###############################################
                
    with tab4:
        st.subheader("Participant Debrief")

        # Information shown to participants if Task 2 is not complete.
        if not st.session_state.task2_complete:
            st.warning("Please complete Task 2 to view the debrief.")

        # Debrief information shown to participants once Task 2 is complete.
        else:
            st.write("""
            Debrief statement: Thank you for participating in this stage of the study. Please follow the link to the final survey, this will only take 5-10 minutes of your time. Please copy your ID number and save it for the start of the survey. [link to final survey].
            """)

############################################### End #################################################

if __name__ == "__main__":
    main()
