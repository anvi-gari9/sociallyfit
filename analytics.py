import streamlit as st
import pandas as pd
import altair as alt
from database import get_workouts

def analytics():
    st.header('Progress Analytics')

    workout_list = get_workouts()

    if workout_list:
        workout_df = pd.DataFrame(workout_list)
        workout_df['date'] = pd.to_datetime(workout_df['date'])

        # Define muscle groups
        muscle_groups = workout_df['muscle_group'].unique()

        # Dropdown for muscle group selection
        selected_muscle_group = st.selectbox('Select a muscle group:', muscle_groups)

        # Filter exercises based on selected muscle group
        filtered_exercises = workout_df[workout_df['muscle_group'] == selected_muscle_group]['exercise'].unique()

        # Dropdown for exercise selection
        selected_exercise = st.selectbox('Select an exercise:', filtered_exercises)

        # Filter data based on selected exercise
        filtered_df = workout_df[workout_df['exercise'] == selected_exercise]

        if not filtered_df.empty:
            # Weight Progression Over Time
            weight_progression = filtered_df.groupby('date')['weight'].sum().reset_index()
            weight_progression_chart = alt.Chart(weight_progression).mark_line(point=True).encode(
                x=alt.X('yearmonthdate(date):T', title='Date', axis=alt.Axis(format='%b %d')),
                y=alt.Y('weight:Q', title='Weight (lbs)'),
                tooltip=[alt.Tooltip('date:T', title='Date', format='%b %d, %Y'), alt.Tooltip('weight:Q', title='Weight (lbs)')]
            ).properties(
                title='Weight Progression Over Time',
                width=600,
                height=400
            )
            st.altair_chart(weight_progression_chart)

            # Set Progression Over Time
            set_progression = filtered_df.groupby('date')['sets'].sum().reset_index()
            set_progression_chart = alt.Chart(set_progression).mark_line(point=True).encode(
                x=alt.X('yearmonthdate(date):T', title='Date', axis=alt.Axis(format='%b %d')),
                y=alt.Y('sets:Q', title='Sets'),
                tooltip=[alt.Tooltip('date:T', title='Date', format='%b %d, %Y'), alt.Tooltip('sets:Q', title='Sets')]
            ).properties(
                title='Set Progression Over Time',
                width=600,
                height=400
            )
            st.altair_chart(set_progression_chart)

            # Rep Progression Over Time
            rep_progression = filtered_df.groupby('date')['reps'].sum().reset_index()
            rep_progression_chart = alt.Chart(rep_progression).mark_line(point=True).encode(
                x=alt.X('yearmonthdate(date):T', title='Date', axis=alt.Axis(format='%b %d')),
                y=alt.Y('reps:Q', title='Reps'),
                tooltip=[alt.Tooltip('date:T', title='Date', format='%b %d, %Y'), alt.Tooltip('reps:Q', title='Reps')]
            ).properties(
                title='Rep Progression Over Time',
                width=600,
                height=400
            )
            st.altair_chart(rep_progression_chart)
        else:
            st.write("No data available for the selected exercise.")
    else:
        st.write("No workout data available for analytics.")

