
# WITH DATABASE SETUP
import streamlit as st
from datetime import datetime
from database import Session, User, Post, Comment
import os  # For file operations

# Name of the signed-in user (the app has no login yet)
CURRENT_USER = "Demo User"

# Initialize database session
session = Session()

# Mock data for friends and friend requests
friends = [
    {"name": "Alice", "image": "images/pfp2.svg"},
    {"name": "Bob", "image": "images/pfp4.png"},
    {"name": "Charlie", "image": "images/pfp3.webp"}
]

friend_requests = [
    {"name": "David", "image": "images/pfp4.png"},
    {"name": "Emma", "image": "images/pfp2.svg"}
]

other_users = [
    {"name": "Frank", "image": "images/pfp2.svg"},
    {"name": "Grace", "image": "images/pfp3.webp"},
    {"name": "Henry", "image": "images/pfp2.svg"}
]
all_users = friends + friend_requests + other_users

def social_network():
    st.title("Social Network")

    # Create tabs
    tab1, tab2 = st.tabs(["Feed", "Friends"])

    # Feed Section
    with tab1:
        st.subheader("Post")
        if 'workout_caption' not in st.session_state:
            st.session_state.workout_caption = ""

        with st.form("post_form_unique"):  # Ensure the form key is unique
            post_date = st.date_input("Date", value=datetime.now(), key="post_date")
            get_workout = st.form_submit_button("Get Today's Workout Snapshot")
            caption = st.text_area("Caption", value=st.session_state.workout_caption, key="caption")
            image = st.file_uploader("Upload Image", type=["png"])
            post_submit = st.form_submit_button("Post")

        if get_workout:
            # Fetch workouts for the selected date
            workouts_for_date = [workout for workout in st.session_state.workouts if workout['date'] == post_date]
            if workouts_for_date:
                workout_details = "\n".join([f"Exercise: {workout['exercise']}, Weight: {workout['weight']} kg, Sets: {workout['sets']}, Reps: {workout['reps']}" for workout in workouts_for_date])
                st.session_state.workout_caption = f"Workout for {post_date.strftime('%b %d, %Y')}:\n{workout_details}"
            else:
                st.warning("No workouts recorded for this date.")
            # Rerun to update the caption field
            st.rerun()

        if post_submit:
            user = session.query(User).filter_by(name=CURRENT_USER).first()
            if not user:
                user = User(name=CURRENT_USER)
                session.add(user)
                session.commit()

            # Save image if uploaded
            image_name = None
            if image:
                # Ensure images directory exists
                if not os.path.exists("images"):
                    os.makedirs("images")
                # Save the uploaded file
                image_name = os.path.join("images", image.name)
                with open(image_name, "wb") as f:
                    f.write(image.read())

            post = Post(user_id=user.id, date=post_date, caption=caption, image=image_name)
            session.add(post)
            session.commit()
            st.success("Post created!")

            # Clear caption text area
            st.session_state.workout_caption = ""

        st.markdown("---")
        st.subheader("My Feed")

        # Display Feed
        posts = session.query(Post).order_by(Post.date.desc(), Post.id.desc()).all()  # Newest posts first
        for post in posts:
            container = st.container()
            container.write(f"Posted by: {post.user.name} - Date: {post.date}")
            container.write(post.caption)
            if post.image:  # Check if image is not None
                try:
                    container.image(post.image, caption=post.caption)
                except Exception as e:
                    container.warning(f"Error displaying image: {e}")

            # Display Comments Section
            if post.comments:
                comment_container = container.container()
                for comment in post.comments:
                    comment_container.write(f"{comment.user.name}: {comment.content}")

            # Like and Comment Section
            col1, col2 = st.columns([6, 1])

            # Comment input and submit button
            with col1:
                comment_text = st.text_input("Add a comment", key=f"comment_text_{post.id}")
            with col2:
                if st.button("Comment", key=f"comment_button_{post.id}"):
                    if comment_text.strip() != "":
                        user = session.query(User).filter_by(name=CURRENT_USER).first()  # Ensure user is always fetched
                        if not user:
                            user = User(name=CURRENT_USER)
                            session.add(user)
                            session.commit()

                        comment = Comment(post_id=post.id, user_id=user.id, content=comment_text)
                        session.add(comment)
                        session.commit()
                        st.rerun()  # Refresh the page

            # Like button
            if col2.button(f"Like ({post.likes})", key=f"like_button_{post.id}"):
                post.likes += 1
                session.commit()
                st.rerun()  # Refresh UI to update like count

    with tab2:
        st.subheader("Friends")

        # Search functionality
        search_query = st.text_input("Search friends by name")
        filtered_friends = [friend for friend in friends if search_query.lower() in friend['name'].lower()]

        # Display filtered friends or all friends if no search query
        friends_to_display = filtered_friends if search_query else friends

        # Display existing friends
        for friend in friends_to_display:
            friend_col1, friend_col2, friend_col3 = st.columns([1, 4, 1])
            with friend_col1:
                st.image(friend["image"], width=50, caption="")
            with friend_col2:
                st.write(friend["name"])

            # Remove friend button
            with friend_col3:
                if st.button("Remove", key=f"remove_friend_button_{friend['name']}"):
                    friends.remove(friend)
                    st.rerun()  # Update UI after removing friend

        st.markdown("---")

        # Manage Friends button
        with st.expander("Manage Friends"):
            st.markdown("**Requests**")

            if len(friend_requests) == 0:
                st.write("No pending requests.")

            for request in friend_requests:
                request_col1, request_col2, request_col3 = st.columns([1, 3, 2])
                with request_col1:
                    st.image(request["image"], width=50, caption="")
                with request_col2:
                    st.write(request["name"])
                with request_col3:
                    if st.button("✓", key=f"approve_button_{request['name']}"):  # Unique key for approval
                        friends.append(request)
                        friend_requests.remove(request)
                        st.rerun()  # Update UI after approval
                    if st.button("❌", key=f"reject_button_{request['name']}"):  # Unique key for rejection
                        friend_requests.remove(request)
                        st.rerun()  # Update UI after rejection

            st.markdown("**Find New Friends**")

            # Search for new users
            search_new_users = st.text_input("Search new users by name")
            filtered_users = [user for user in all_users if search_new_users.lower() in user['name'].lower()]

            # Display filtered users only when searched
            if search_new_users:
                for user in filtered_users:
                    user_col1, user_col2, user_col3 = st.columns([1, 3, 1])
                    with user_col1:
                        st.image(user["image"], width=50, caption="")
                    with user_col2:
                        st.write(user["name"])
                    with user_col3:
                        if st.button("Add Friend", key=f"add_friend_button_{user['name']}"):
                            friends.append(user)  # Add user directly to friends list
                            st.rerun()  # Update UI after adding friend

