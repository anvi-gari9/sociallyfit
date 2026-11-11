import streamlit as st
from datetime import datetime, timedelta
from social_network import social_network
from workout_logging import workout_logging
from analytics import analytics
from ai_workout_planning import ai_workout_planning
from ai_recipe_meals import ai_recipe_meals
from challenges_milestones import challenges_milestones

# Initialize session state for storing workouts and exercises
if 'workouts' not in st.session_state:
    st.session_state.workouts = []
if 'exercises' not in st.session_state:
    st.session_state.exercises = []
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = None
if 'current_week_start' not in st.session_state:
    st.session_state.current_week_start = datetime.now().date() - timedelta(days=datetime.now().date().weekday())

# Function to add a new exercise input
# def add_exercise():
#     st.session_state.exercises.append({"exercise": "", "weight": 0, "sets": 0, "reps": 0})

# # Function to get workouts for a specific date
# def get_workouts_for_date(workout_date):
#     return [workout for workout in st.session_state.workouts if workout['date'] == workout_date]

# # Function to display the current week's calendar
# def display_current_week():
#     current_week_start = st.session_state.current_week_start
#     selected_date = st.session_state.selected_date

#     # Ensure selected_date is within the current displayed week
#     if selected_date and not (current_week_start <= selected_date < current_week_start + timedelta(days=7)):
#         st.session_state.selected_date = None

#     # Display month and navigation arrows in a single line
#     col1, col2, col3 = st.columns([1, 6, 1])
#     with col3:
#         if st.button(">", key="next_week"):
#             st.session_state.current_week_start += timedelta(days=7)
#             st.session_state.selected_date = None  # Reset selected_date on week change
#             st.experimental_rerun()  # Force rerun to update UI
#     with col1:
#         if st.button("<", key="prev_week"):
#             st.session_state.current_week_start -= timedelta(days=7)
#             st.session_state.selected_date = None  # Reset selected_date on week change
#             st.experimental_rerun()  # Force rerun to update UI
#     with col2:
#         st.subheader(current_week_start.strftime("%B %Y"))

#     st.write("")
#     st.markdown("---")

#     columns = st.columns(7)
#     day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

#     # Display day names
#     for i, day_name in enumerate(day_names):
#         with columns[i]:
#             st.write(day_name)

#     # Display dates and workouts for the current week
#     for i in range(7):
#         day = current_week_start + timedelta(days=i)
#         workouts_for_day = get_workouts_for_date(day)
#         with columns[i]:
#             if workouts_for_day:
#                 if st.button(str(day.day), key=day.strftime("%Y-%m-%d"), help="Click to see details"):
#                     st.session_state.selected_date = day  
#             else:
#                 if st.button(str(day.day), key=day.strftime("%Y-%m-%d")):
#                     st.session_state.selected_date = day  

# Home Page
def home():
    st.title("SociallyFit")
    st.write("Welcome to SociallyFit! Track your workouts, meals, and connect with friends.")

    # Adding an image
    st.image("images/fitness_image.png", width="stretch")

    # st.subheader("Log Today's Workout")

    # # Input form for weight lifting workout
    # with st.form("workout_form"):
    #     date = st.date_input("Date", value=datetime.now(), key="workout_date")

    #     # Display exercise inputs
    #     for idx, exercise in enumerate(st.session_state.exercises):
    #         exercise_name = st.text_input("Exercise", key=f"exercise_name_{idx}")
    #         weight = st.number_input("Weight (kg)", min_value=0, key=f"weight_{idx}")
    #         sets = st.number_input("Sets", min_value=0, key=f"sets_{idx}")
    #         reps = st.number_input("Reps", min_value=0, key=f"reps_{idx}")
    #         st.session_state.exercises[idx] = {"exercise": exercise_name, "weight": weight, "sets": sets, "reps": reps}

    #     # Columns for buttons
    #     col1, col2 = st.columns([1, 4])
    #     with col1:
    #         add_button = st.form_submit_button("Add Exercise", on_click=add_exercise)
    #     with col2:
    #         submit = st.form_submit_button("Record Workout")
    #         if submit:
    #             # Store the workout data
    #             for exercise in st.session_state.exercises:
    #                 st.session_state.workouts.append({"date": date, **exercise})
    #             st.session_state.exercises = []  
    #             st.success("Workout recorded!")
    #             st.experimental_rerun()  

    # # Display the calendar
    # st.subheader("Workout Calendar")
    # st.write("Take a look at your past workouts")

    # st.write("")  # Placeholder for layout
    # display_current_week()

    # # Display workouts for the selected date
    # if st.session_state.selected_date:
    #     selected_date = st.session_state.selected_date
    #     st.subheader(f"Workouts for {selected_date.strftime('%b %d, %Y')}")
    #     workouts_for_selected_date = get_workouts_for_date(selected_date)
    #     if workouts_for_selected_date:
    #         for workout in workouts_for_selected_date:
    #             st.write(f"**Exercise:** {workout['exercise']}")
    #             st.write(f"**Weight:** {workout['weight']} kg")
    #             st.write(f"**Sets:** {workout['sets']}")
    #             st.write(f"**Reps:** {workout['reps']}")
    #             st.markdown("---")  # Separator between workouts
    #     else:
    #         st.info("No workouts recorded for this date.")

# Define pages
pages = {
    "Home": home,
    "AI Workout Planning": ai_workout_planning,
    "Network": social_network,
    "Challenges and Milestones": challenges_milestones,
    "AI Meal Planning, Recipes, and Fitness Advice": ai_recipe_meals,
    "Workout Logging": workout_logging,
    "Analytics": analytics
}

# Navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()), index=0)

# Run selected page
pages[selection]()

