# python3 -m streamlit run app.py 


import streamlit as st

import base64
import requests

SYSTEM_PROMPT = """You are a botany expert who provides expert advice on how to keep plants healthy. You determine what plant the user took a photo of and use the image to diagnose issues. Use this information in combination with the user message, which includes a description of the issue. Potential issues may include desease, overwatering, underwatering, too much sun, not enough humidity, etc. Provide useful tips to the user so they can have a healthy plant. If you don't know,just say "I'm not sure how to help, sorry"."""

def getResponse(user_message, bytes):

    base64_image = base64.b64encode(bytes).decode()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": user_message
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()


st.write("""# 🌱 Plant Daddy""")

st.header("Upload a photo of your plant baby. I'll figure out how to heal it.")

uploaded_file = st.file_uploader("Upload an image", accept_multiple_files=False)

text_input = st.text_input("Describe what's wrong 🥺")

if st.button("Go", type="primary"):
    if uploaded_file is not None:
        st.write(f"Analyzing: {uploaded_file.name}")
        bytes_data = uploaded_file.getvalue()
        response = getResponse(text_input, bytes_data)
        st.header("Plant daddy's diagnosis.")
        st.write(response["choices"][0]["message"]["content"])










