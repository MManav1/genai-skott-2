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

import anthropic

def generate_content_with_claude(keywords):
    client = anthropic.Anthropic(api_key=st.secrets["claude_api_key"])

    prompt = f"""
    Short tail and long tail keywords: {keywords}
    
    Using the provided keywords and best performing paragraphs, create an engaging and extensive blog post.
    """

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system="You will be given a set of short tail and long tail keywords on a given topic, plus the best performing paragraphs of that blog. Take that information and create an engaging but extensive blog by yourself.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content

# Example usage:
# api_key = "your_api_key_here"
# keywords = "SEO, content marketing, blog optimization"
# best_paragraphs = "Paragraph 1... Paragraph 2..."
# content = generate_content_with_claude(api_key, keywords, best_paragraphs)
# print(content)

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
