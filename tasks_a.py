# Importing required modules.
import json
import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np 
import pandas as pd
import time

# Authenticating google sheets file for remote data saving.

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Loading credentials from Streamlit secrets.
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(creds)

# Trying to open sheet.
spreadsheet = client.open("participant_data")
sheet = spreadsheet.sheet1

# Saving data function.

def save_task_dat():
    """
    Saves participant data to a Google Sheet.

    This function collects relevant information from streamlits session state, creates list with the data, and saves it to the Google Sheet.
    """
    # Getting participants memorable word, "unknown" if not entered.
    memorable_word = st.session_state.get("ID_input", "unknown")
    # Participants on this page are in Group A.
    group = "A"
    # Retrieving the participants coding confidence.
    confidence = st.session_state.get("coding_confidence", None)
    # Getting the time taken to complete Task 1.
    task1_time = st.session_state.get("task1_duration", None)
    # Converting Task 1 success to a binary result (1 for correct, 0 for incorrect or error).
    task1_result = 1 if st.session_state.get("task1_success", False) else 0
    # Retrieving Task 2 time.
    task2_time = st.session_state.get("task2_duration", None)
    # Retrieving Task 2 score.
    task2_result = 1 if st.session_state.get("task2_success", False) else 0

    # Organising data into a list to match sheet columns.
    row = [
        memorable_word,
        group,
        confidence,
        task1_time,
        task1_result,
        task2_time,
        task2_result
    ]
    st.write("saving row:", row)
    
    try:
        # Appending new row to Google Sheet
        sheet.append_row(row)
        st.success("Your responses have been saved successfully!")
    except Exception as e:
        st.error(f"Failed to save data: {e}")
    
# Intialising main function.

def main():
    st.title("Coding Tasks")

##################################### Variables #################################

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
        In this activity, you will complete **two short Python coding challenges**.

        **Timing and Structure:**
        - You will be **timed automatically** as soon as you click "Start Task" on the task tabs.
        - You have **one attempt** to submit your code for each task.
        - Take as long as you need, but note that the timer only stops once you submit the task.
        - **Task 2 will unlock only after Task 1 is completed**. Feel free to take a break between tasks.

        Please complete the tasks as you naturally would under these conditions.
        """)

        # Slider to mark confidence level in python coding.
        st.write("How confident are you at writing Python code?")
        coding_confidence = st.slider("0 being extremely **unconfident** and 5 being extremely **confident**.", 0, 5, 1)
        st.write(f"I mark my Python coding confidence at {coding_confidence} out of 5.")

        # For csv file.
        if st.button("Save confidence level."):
            # Storing the current value of coding_confidence in the session state.
            st.session_state.coding_confidence = coding_confidence
            # Displaying success message to confirm value was saved.
            st.success("Confidence level saved!")

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
            st.info(f"Thank you for completing Task 1 (time taken: {st.session_state.task1_duration:.2f} seconds), please take a short break and then move onto Task 2.")
            st.warning("Task 1 is now locked.")
            
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
            with st.expander("Click here for more information."):
                st.write("""
            Use the box below to:
            
            Step 1. Read each line and extract speed.
            
            Step 2. Compare each speed to the previous one. 
            
            Step 3. Count cases where the difference is strictly greater than 30.
            """)
              
            # Form to record participants answer.
            with st.form(key="a_task_1_form"):
                # Logging Task 1 answer.
                task1_answer = st.text_area("Enter Python Code Here")
                # Generating submit button.
                submit_button1 = st.form_submit_button(label="Submit")

            # Important reminders for participants.
            st.write("You only get **ONE ATTEMPT** at submitting your code. Please read through it carefully.")
            st.write("**INDENTATION MATTERS** write this code as you would any other Python code.")
            st.write("Assign your answer to the variable name 'result', e.g. **result = YOUR_ANSWER**.")
            
            if submit_button1:
                # Logging Task 1 end time.
                st.session_state.task1_end_time = time.time()
                # Calculating Task 1 duration.
                st.session_state.task1_duration = (
                    st.session_state.task1_end_time - st.session_state.task1_start_time
                )
                
                # Calculating correct answer for Task 1.
                task1_correct = 0
                # Converting "Speed" column from DataFrame into a list of speeds.
                speeds = df["Speed"].tolist()
                # Looping through the speeds list starting from second item.
                for i in range(1, len(speeds)):
                    # Checking if the speed is more than 30 units higher than the previous.
                    if speeds[i] - speeds[i - 1] > 30:
                        # Increment counter if condition is met.
                        task1_correct += 1

                # Running participants code and extracting results.
                try:
                    # Isolating participants result.
                    # Dictionary to hold variables defined during execution of participants code.
                    local_vars = {}
                    # Executing the participants submitted code for Task 1.
                    exec(task1_answer, {}, local_vars)
                    # Retrieving the result variable from the executed code.
                    user_result = local_vars.get("result", None)

                    # Storing results in session state variables.
                    st.session_state.task1_user_result = user_result
                    st.session_state.task1_correct_result = task1_correct
                    # Comparing participants result to the correct one and store whether its correct.
                    st.session_state.task1_success = (user_result == task1_correct)
               
                # Catching any errors in the participants code.
                except Exception as e:
                    # Setting result to None if theres and error.
                    user_result = None
                    # Recording the error message in the session state for participants feedback.
                    st.session_state.task1_user_result = f"Error: {e}"
                    st.session_state.task1_correct_result = task1_correct
                    # Mark task as unsuccessful.
                    st.session_state.task1_success = False
                    
                # Logging Task 1 as complete.
                st.session_state.task1_complete = True
                # Rerunning the code so that new information is shown to participants.
                st.rerun()

        # What participants see before having access to Task 1.
        else:
            # Information for participants regarding Task 1.
            st.write("""
            ### Conditions

            - The use of ChatGPT is **encouraged**.
            - The task will load and you will be **timed automatically** as soon as you click "Start Task".
            - You have **one attempt** to submit your code.
            - Take as long as you need, but note that the timer only stops when you hit "Submit".

            When you are ready, please click "Start Task".
            """)

            # Form to record participants understand Task 1 rules.
            with st.form(key="a_info_1_form"):
                info1_submit = st.form_submit_button(label="Start Task.")

            if info1_submit:
                # Logging Task 1 as started.
                st.session_state.task1_started = True
                # Rerunning the code so that participants have access to Task 1.
                st.rerun()

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
            st.info(f"Thank you for completing Task 2 (time taken: {st.session_state.task2_duration:.2f} seconds). You may now proceed to the debrief tab.")
            st.warning("Task 2 is now locked.")

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
            with st.expander("Click here for more information."):
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

            # Important reminders for participants.
            st.write("You only get **ONE ATTEMPT** at submitting your code. Please read through it carefully.")
            st.write("**INDENTATION MATTERS** write this code as you would any other Python code.")
            st.write("Assign your answer to the variable name 'result', e.g. **result = YOUR_ANSWER**.")
            
            if submit_button2:
                # Logging Task 2 end time.
                st.session_state.task2_end_time = time.time()
                # Calculating Task 2 duration.
                st.session_state.task2_duration = (
                    st.session_state.task2_end_time - st.session_state.task2_start_time
                )
                
                # Calculating correct answer.
                # Converting columns to lists.
                speeds = df["Speed"].tolist()
                timestamps = df.index.tolist()
                # Initialising variable to store the longest duration of increasing speeds.
                max_duration = 0
                # Starting index of current increasing sequence.
                start = 0

                # Looping through the speeds starting from second item.
                for i in range(1, len(speeds)):
                    if speeds[i] > speeds[i - 1]:
                        # If current speed is higher than the previous, continue sequence.
                        continue
                    else:
                        # Calculating duration of the next increasing sequence if current sequence breaks (speed doesnt increase).
                        duration = timestamps[i - 1] - timestamps[start]
                        # Updating max_duration if this one is longer.
                        if duration > max_duration:
                            max_duration = duration
                        # Resetting the start index if this one is longer.
                        start = i
                # Final check after loop.
                duration = timestamps[-1] - timestamps[start]
                if duration > max_duration:
                    max_duration = duration

                # Running participants code and extracting results.
                try:
                    # Isolating participants results.
                    # Dictionary to store variables from participants code.
                    local_vars = {}
                    # Executing the submitted Task 2 code safely.
                    exec(task2_answer, {}, local_vars)
                    # Retrieving the participants result from code.
                    user_result = local_vars.get("result", None)

                    # Storing results in session state variables.
                    st.session_state.task2_user_result = user_result
                    st.session_state.task2_correct_result = max_duration
                    # Checking if participants results match correct answer.
                    st.session_state.task2_success = (user_result == max_duration)

                # Catching any errors in the participants code.
                except Exception as e:
                    # No result if theres an error.
                    user_result = None
                    # Storing error message and marking task as unsuccessful.
                    st.session_state.task2_user_result = f"Error: {e}"
                    st.session_state.task2_correct_result = max_duration
                    st.session_state.task2_success = False
                    
                # Logging Task 2 as complete.
                st.session_state.task2_complete = True
                # Rerunning the code so that new information is shown to participants.
                st.rerun()

        # What participants see before having acces to Task 2.
        if st.session_state.task1_complete and not st.session_state.task2_complete and not st.session_state.task2_started:
            
            # Information for participants regarding Task 2.
            st.write("""
            ### Conditions

            -  **DO NOT** use external tools, such as ChatGPT. The use of external tools is **strictly prohibited**.
            - The task will load and you will be **timed automatically** as soon as you click "Start Task".
            - You have **one attempt** to submit your code.
            - Take as long as you need, but note that the timer only stops when you hit "Submit".

            When you are ready, please click "Start Task".
            """)
            
            # Form to record participants understand Task 2 rules.
            with st.form(key="a_info_2_form"):
                info2_submit = st.form_submit_button(label="Start Task.")

            if info2_submit:
                # Logging Task 2 as started.
                st.session_state.task2_started = True
                # Rerunning the code so that participants have access to Task 2.
                st.rerun()
            
############################################# Debrief ###############################################
                
    with tab4:
        st.subheader("Participant Debrief")

        # Information shown to participants if Task 2 is not complete.
        if not st.session_state.task2_complete:
            st.warning("Please complete Task 2 to view the debrief.")

        # Debrief information shown to participants once Task 2 is complete.
        else:
            st.write("""
            Thank you for taking part in this stage of the study!

            Please follow the link below to complete a short final survey (5-10 minutes).
            
            **Remember you will need your memorable word for the final survey.**

            https://forms.cloud.microsoft/e/HBS5YbGGVN

            Once again, thank you for your time and participation!
            """)
            # Checking if "results_saved" session state is set.
            if not st.session_state.get("results_saved", False):
                # Calling function to save task data.
                save_task_dat()
                # Setting "results_saved" to True to avoide re-saving.
                st.session_state.results_saved = True
                # Showing a success message to participants.
                st.success("Your responses have been saved successfully!")


############################################### End #################################################

if __name__ == "__main__":
    main()
