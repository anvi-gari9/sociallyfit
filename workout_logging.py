import streamlit as st
import requests
from datetime import date
import pandas as pd
import os
from dotenv import load_dotenv
from database import add_workout, get_workouts

load_dotenv()

def workout_logging():
    st.header('Workout Logging and Tracking')

    API_KEY = os.getenv('API_NINJAS_KEY')

    def get_exercises(muscle):
        url = f'https://api.api-ninjas.com/v1/exercises?muscle={muscle}'
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                st.error("Error decoding the JSON response")
                return None
        else:
            st.error(f"Error fetching exercises: {response.status_code}")
            st.write(response.text)
            return None
        
    # Initialize session state for exercises and exercise_names if not already done
    if 'exercises' not in st.session_state:
        st.session_state['exercises'] = []
    if 'exercise_names' not in st.session_state:
        st.session_state['exercise_names'] = ["No exercises available"]

    # Define muscle groups
    muscle_groups = [
        'chest', 'back', 'legs', 'arms', 'shoulders', 'abs'
    ]

    # Dropdown for muscle group selection
    muscle = st.selectbox('Select a muscle group:', muscle_groups)

    # Fetch exercises button
    if st.button('Fetch Exercises'):
        exercises = get_exercises(muscle)
        if exercises:
            st.session_state['exercises'] = exercises
            st.session_state['exercise_names'] = [exercise['name'] for exercise in exercises]
            st.success("Exercises fetched successfully!")

    exercise_names = st.session_state['exercise_names']

    # Dropdown for exercise selection
    selected_exercise = st.selectbox('Select an exercise:', exercise_names)

    # Manual exercise entry
    st.subheader('Or Enter Exercise Manually')
    manual_exercise_name = st.text_input('Exercise Name')
    manual_muscle_group = st.selectbox('Muscle Group', muscle_groups, key='manual_muscle')
    is_manual_entry = st.checkbox('Use manually entered exercise')

    # Logging workouts
    st.header('Log Your Workout')
    sets = st.number_input('Sets', min_value=1, max_value=10, step=1)
    reps = st.number_input('Reps', min_value=1, max_value=50, step=1)
    weight = st.number_input('Weight (lbs)', min_value=0.0, max_value=1000.0, step=0.5)
    workout_date = st.date_input('Date', value=date.today())

    if st.button('Log Workout'):
        if is_manual_entry and manual_exercise_name:
            workout = {
                'exercise': manual_exercise_name,
                'muscle_group': manual_muscle_group,
                'sets': sets,
                'reps': reps,
                'weight': weight,
                'date': workout_date
            }
            add_workout(workout)
            st.success('Workout logged successfully!')
        elif selected_exercise != "No exercises available":
            workout = {
                'exercise': selected_exercise,
                'muscle_group': muscle,
                'sets': sets,
                'reps': reps,
                'weight': weight,
                'date': workout_date
            }
            add_workout(workout)
            st.success('Workout logged successfully!')
        else:
            st.error('Please select a valid exercise or enter one manually.')

    # Display logged workouts in calendar format
    st.header('Logged Workouts')

    workout_list = get_workouts()

    if workout_list:
        workout_df = pd.DataFrame(workout_list)
        workout_df['date'] = pd.to_datetime(workout_df['date'])
        workout_dates = workout_df['date'].dt.date.unique()
        
        # Check if workout_dates is not empty before setting date input limits
        if workout_dates.size > 0:
            selected_date = st.date_input('Select a date to view workouts', value=max(workout_dates), min_value=min(workout_dates), max_value=max(workout_dates))

            if selected_date in workout_dates:
                st.write(f"Workouts for {selected_date}:")
                day_workouts = workout_df[workout_df['date'].dt.date == selected_date]
                for _, workout in day_workouts.iterrows():
                    st.write(f"Exercise: {workout['exercise']}, Muscle Group: {workout['muscle_group']}, Sets: {workout['sets']}, Reps: {workout['reps']}, Weight: {workout['weight']} lbs")
        else:
            st.write("No workouts available to display.")
    else:
        st.write("No workouts logged yet.")

    # CSS for custom button
    st.markdown(
        """
        <style>
        .custom-button {
            background-color: rgb(241, 174, 174);
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
