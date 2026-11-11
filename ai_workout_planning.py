from openai import OpenAI
import streamlit as st
import json
import time

import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_fallback_plans():
    try:
        with open("fallback_plans.json", "r") as file:
            fallback_plans = json.load(file)
        return fallback_plans
    except FileNotFoundError:
        return []

def query(prompt, instructions, retries=3):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": prompt}
                ]
            )
            output = response.choices[0].message.content.strip()
            return output
        except Exception as error:
            if attempt < retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                print("Error:", error)  # Debug: print error
                return f"Oops, something went wrong: {error}"

def ai_workout_planning():
    st.title("AI-Powered Workout Planning")
    st.write("Get a personalized workout plan based on your goals and preferences.")

    # Adding an image
    st.image("images/fitness_image.png", width="stretch")

    # User inputs
    fitness_level = st.selectbox("Select your fitness level:", ["Select an option", "Beginner", "Intermediate", "Advanced"])
    goals = st.selectbox("Choose your fitness goals:", ["Select an option", "Lose weight", "Build muscle", "Improve endurance", "Increase flexibility", "Maintain health"])
    workout_types = st.multiselect("Select your workout preferences:", ["Cardio", "Strength training", "Yoga", "Stretching", "Other"])
    frequency = st.select_slider(
        "How often do you want to workout?",
        options=["1-2 times a week", "3-4 times a week", "5-6 times a week", "Every day"],
        value="3-4 times a week"  # Default value
    )

    # Generate workout plan
    if st.button("Get Workout Plan"):
        if fitness_level != "Select an option" and goals != "Select an option" and workout_types and frequency:
            with st.spinner("Generating workout plan..."):
                prompt = (
                    f"Create a personalized workout plan for a person with the following details:\n\n"
                    f"Fitness Level: {fitness_level}\n"
                    f"Goals: {goals}\n"
                    f"Workout Types: {', '.join(workout_types)}\n"
                    f"Workout Frequency: {frequency}\n\n"
                    "Plan:"
                )
                plan = query(prompt, "You are a helpful fitness assistant.")
                
                if "Oops, something went wrong" in plan:
                    st.error(plan)
                    st.write("Using fallback workout plan...")
                    fallback_plans = load_fallback_plans()
                    if fallback_plans:
                        st.subheader("Fallback Workout Plan")
                        st.write(fallback_plans[0])
                    else:
                        st.error("No fallback plans available.")
                else:
                    st.subheader("Your Personalized Workout Plan")
                    st.write(plan)
                    
                    # Get warm-up and cool-down routines
                    with st.spinner("Generating warm-up and cool-down routines..."):
                        routines_prompt = (
                            f"Create personalized warm-up and cool-down routines for the following workout plan:\n\n"
                            f"{plan}\n\n"
                            "Warm-up and Cool-down routines:"
                        )
                        routines = query(routines_prompt, "You are a helpful fitness assistant.")
                        st.subheader("Warm-Up and Cool-Down Routines")
                        st.write(routines)

# Ensure to call ai_workout_planning if this script is run directly
if __name__ == "__main__":
    ai_workout_planning()
