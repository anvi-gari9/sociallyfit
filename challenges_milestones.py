import streamlit as st
import pandas as pd

def mark_challenge_completed(idx):
    st.session_state.completed_challenges.append(st.session_state.challenges.pop(idx))

def challenges_milestones():
    # Initialize session state for challenges and completed challenges
    if 'challenges' not in st.session_state:
        st.session_state.challenges = []
    if 'completed_challenges' not in st.session_state:
        st.session_state.completed_challenges = []

    st.title("Challenges and Milestones")
    st.write("Set and track your personalized fitness challenges and milestones.")
    
    # Adding an image
    st.image("images/challenges_milestones.jpg", width="stretch")

    # Add new challenge
    challenge = st.text_input("Enter a new challenge (e.g., Run 5 miles, Lift 100kg, etc.)")
    milestone = st.number_input("Set a milestone target", min_value=1, value=1, step=1)
    if st.button("Add Challenge"):
        st.session_state.challenges.append({"challenge": challenge, "milestone": milestone})
        st.success("Challenge added!")

    # Display active challenges
    if st.session_state.challenges:
        st.subheader("Your Challenges and Milestones")
        
        challenge_data = {
            "Challenge": [item["challenge"] for item in st.session_state.challenges],
            "Milestone": [item["milestone"] for item in st.session_state.challenges],
            "Action": [f"Complete_{idx}" for idx in range(len(st.session_state.challenges))]
        }
        df_challenges = pd.DataFrame(challenge_data)
        
        for idx, row in df_challenges.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"{row['Challenge']}")
            with col2:
                st.write(f"Target: {row['Milestone']}")
            with col3:
                if st.button("Mark as Completed", key=row["Action"]):
                    mark_challenge_completed(idx)
                    st.experimental_rerun()

    # Display completed challenges
    if st.session_state.completed_challenges:
        st.subheader("Completed Challenges")
        
        completed_data = {
            "Challenge": [item["challenge"] for item in st.session_state.completed_challenges],
            "Milestone": [item["milestone"] for item in st.session_state.completed_challenges]
        }
        df_completed = pd.DataFrame(completed_data)
        
        st.table(df_completed)

