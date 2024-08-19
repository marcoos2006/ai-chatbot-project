import os
import streamlit as st
from streamlit_js_eval import get_geolocation
from dotenv import load_dotenv
import random  # To generate simulated ratings
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Yummy Food Nearby",
    page_icon="🍴",  # Favicon emoji related to food
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
instruction = """
You are a Restaurant Bot. You assist users with finding restaurants, providing restaurant recommendations, 
answering questions about menu items, opening hours, and reviews.
Although you do not have real-time data, you can simulate helpful responses based on general restaurant knowledge.
You can also simulate restaurant reviews and ratings on a scale of 1 to 5 stars.
"""
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

# Fetch user's geolocation
location = get_geolocation()

# Display the user's geolocation
if location:
    st.write("Your location:", location)
else:
    st.write("Location could not be determined.")

# Function to simulate star ratings for restaurants
def simulate_star_rating(restaurant_name):
    return random.randint(1, 5)  # Simulates a random star rating between 1 and 5

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🍴 Restaurant Chatbot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask about restaurants, reviews, or anything food-related...") 
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Check if the user is asking for a review or rating of a restaurant
    if "review" in user_prompt.lower() or "rating" in user_prompt.lower():
        # Simulate a restaurant name extraction (for simplicity, use the full prompt as the restaurant name)
        restaurant_name = user_prompt.replace("review", "").replace("rating", "").strip()
        if restaurant_name:
            # Simulate a star rating for the restaurant
            rating = simulate_star_rating(restaurant_name)
            response_text = f"The restaurant '{restaurant_name}' has a rating of {rating} stars."
        else:
            response_text = "Please specify the name of the restaurant you'd like to get a review for."
    else:
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        response_text = gemini_response.text

    # Display Gemini-Pro's response or the simulated rating
    with st.chat_message("assistant"):
        st.markdown(response_text)

# Example queries the chatbot can handle
st.write("💡 Try asking things like:")
st.write("- 'What are some good Italian restaurants?'")
st.write("- 'Can you recommend a dish?'")
st.write("- 'What is a typical dinner menu in a French restaurant?'")
st.write("- 'Tell me about popular restaurants in New York City.'")
st.write("- 'Can I get a review of a specific restaurant?'")