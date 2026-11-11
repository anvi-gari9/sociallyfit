from openai import OpenAI


import streamlit as st
import simplejson as json
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Set up OpenAI API key
def query(prompt, instructions):
    try:
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt}
        ])
        output = response.choices[0].message.content.strip()
        return output

    except Exception as error:
        return f"oops, something went wrong!: {error}"

def intro():
    st.title("AI-Powered Fitness Advice, Meal Planning, and Recipe Generation")
    st.write("Get personalized meal prep and recipes, or just ask for fitness advice. Simply select what you want in the sidebar and fill out the forms, or chat directly with a chatbot for fitness advice!")

    # Adding an image
    st.image("images/fitness_image.png", width="stretch")

def custom_recipe():
    st.title("Custom Recipe Builder")
    st.write("Build your own recipe for a healthy meal based on your preferences, restrictions, and goals, simply fill out the form below and hit Submit!")

    # User inputs
    type = st.text_input("Describe the type of meal you are going for in three words (i.e. healthy, cheat meal, thanksgiving dinner, etc.)")
    people = st.select_slider("How many people are you making the meal for?", options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    style = st.selectbox("Select a style of food.", options=["Select an option", "thai", "east asian", "indian", "italian", "american", "mediterranean", "mexican", "suprise me!"])
    allergies = st.text_input("Please list out your allergies (separate them with commas)")
    diet_type = st.text_input("Do are follow any dietary restrictions? Please list them below (separate them with commas)")

    # Generate workout plan
    if st.button("Get Customized Recipe!"):
        if type and style != "Select an option":
            with st.spinner("Generating recipe..."):
                prompt = (
                    f"Create a {type} recipe with the following details:\n\n"
                    f"Cuisine type: {style}\n"
                    f"Numer of people eating: {people}\n"
                )
                if len(allergies) > 0:
                    prompt += f"Allergies: {allergies}\n"
                if len(diet_type) > 0:
                    prompt += f"Dietary Style: {diet_type}\n"

                print(prompt, )
                plan = query(prompt, "You are a helpful recipe creation assistant.")
                if "exceeded your current quota" in plan:
                    st.error(plan)
                else:
                    st.subheader("Your Customized Recipe")
                    st.write(plan)
        else:
            st.error("Please fill in all the details.")

def general_advice():
    st.title("FitnessBot")
    st.write("Get fitness advice and recommendations from a state-of-the-art LLM!")
    instructions="You are a useful fitness chatbot."

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("What's on your mind (fitness related of course!)?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)


        with st.chat_message("assistant"):
            messages = [{"role": "system", "content": instructions}]
            stream = client.chat.completions.create(model=st.session_state["openai_model"],
            messages=messages + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True)
            collected_chunks = []
            collected_messages = []

            for chunk in stream:
                if "content" in chunk.choices[0].delta:
                    collected_messages.append(chunk.choices[0].delta.content)

            collected_messages = [m for m in collected_messages if m is not None]
            response = ''.join(collected_messages)

            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


def meal_planning():
    st.title("Meal Planner")
    st.write("Get a personalized, diet observant, allergen aware meal plan, simply fill out the form below and hit Submit!")

    # User inputs
    sex = st.selectbox("What is your sex?", ["Select an option", "male", "female"])
    fitness_level = st.select_slider("How active are you on a scale of 1-5, where 1 is less than 30 minutes of activity per day and 5 is over 3 hours of activity per day?", options=["1", "2", "3", "4", "5"])
    meal_count = st.selectbox("How many meals do you eat per day?", ["Select an option", "1", "2", "3"])
    weight_goal = st.selectbox("Are you trying to lose weight or gain weight?", ["Select an option", "Heavy cut", "Mild cut", "Maintain", "Mild bulk", "Heavy bulk"])
    allergies = st.text_input("Please list out your allergies (separate them with commas)")
    diet_type = st.text_input("Do are follow any dietary restrictions? Please list them below (separate them with commas)")

    # Generate workout plan
    if st.button("Get Customized Meal Plan!"):
        if meal_count != "Select an option" and weight_goal != "Select an option" and sex != "Select an option":
            with st.spinner("Generating meal plan..."):
                prompt = (
                    f"Create a personalized daily meal plan for a {sex} with the following details:\n\n"
                    f"Fitness Level (1 is sedentary and 5 is extremely active): {fitness_level}\n"
                    f"Daily Number of Meals: {meal_count}\n"
                    f"Weight Target: {weight_goal}\n"
                )
                if len(allergies) > 0:
                    prompt += f"Allergies: {allergies}\n"
                if len(diet_type) > 0:
                    prompt += f"Dietary Style: {diet_type}\n"

                print(prompt)
                plan = query(prompt, "You are a helpful meal planning assistant.")
                if "exceeded your current quota" in plan:
                    st.error(plan)
                else:
                    st.subheader("Your Personalized Meal Plan")
                    st.write(plan)
        else:
            st.error("Please fill in all the details.")

def ai_recipe_meals():
    page_names_to_funcs = {
        "—": intro,
        "Meal Planning": meal_planning,
        "Custom Recipes": custom_recipe,
        "General Advice": general_advice,
    }

    demo_name = st.sidebar.selectbox("What do you want to do?", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()