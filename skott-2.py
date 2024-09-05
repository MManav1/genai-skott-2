import streamlit as st
import requests

import requests

def send_lyzr_chat_message(message, user_id="default_user", agent_id="66d96db817901bc73565f592", session_id="abcd"):
    url = st.secrets["lyzr_url"]
    headers = {
        "Content-Type": "application/json",
        "x-api-key": st.secrets["lyzr_api_key"]
    }
    payload = {
        "user_id": user_id,
        "agent_id": agent_id,
        "session_id": session_id,
        "message": message
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
# api_key = "your_api_key_here"
# result = send_lyzr_chat_message(api_key, "Hello, how are you?")
# if result:
#     print(result)

def generate_content_with_claude(keywords):
    # This function will use Claude to generate content based on the keywords
    prompt = f"Generate SEO content using the following keywords: {', '.join(keywords)}"
    response = requests.post("https://api.claude.ai/generate", json={"prompt": prompt})
    if response.status_code == 200:
        data = response.json()
        content = data.get('content', '')
        return content
    else:
        st.error("Failed to generate content with Claude")
        return ""

def main():
    st.title("SEO Content Writing Agent")
    topic = st.text_input("Enter the topic for SEO content:")
    if topic:
        st.write("Researching competitor keywords...")
        keywords = send_lyzr_chat_message(topic)
        if keywords:
            st.write("Generating content with Claude...")
            content = generate_content_with_claude(keywords)
            if content:
                st.write("Generated Content:")
                st.write(content)

if __name__ == "__main__":
    main()
