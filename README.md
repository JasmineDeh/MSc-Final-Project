# Stage 2 Task Application

This directory contains the code for **Stage 2** of the study, where participants complete problem-solving tasks under different conditions. The system randomly assigns participants to one of two groups (Group A or Group B) when they launch the app.


# File Overview

1. **Welcome_to_Stage_2.py**
   - The main entry point for Stage 2.
   - Built with Streamlit.
   - Handles participant login via their memorable word (entered in Stage 1).
   - Assigns participants to a task group:
     - **Group A:** AI-assisted condition.
     - **Group B:** Non-AI condition.
   - Routes participants to the appropriate task module (*tasks_a.py* or *tasks_b.py*).

2. **tasks_a.py**
   - Contains the task flow for Group A (AI-assisted condition).
   - Includes instructions, task content, and interactive components.
   - Participants work through tasks step by step.
  
3. **task_b.py**
   - Contains the task flow for Group B (non-AI condition).
   - Parallel structure to tasks_a.py, but without AI assistance.


# Running the App Locally

1. **Clone the Repository**

   ```bash
   clone
   cd
   ```

2. **Dependencies**

   Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run in Terminal**

   ```bash
   streamlit run Welcome_to_Stage_2.py
   ```

# Remote Access

If you don't want to run the app locally, you can access it directly here:

(https://welcome-to-stage-2.streamlit.app/)
