import os
import streamlit as st
import requests

base_url = f'http://{os.environ.get("FASTAPI_HOST", "localhost")}:{os.environ.get("FASTAPI_PORT", "8000")}/files'


def get_ai_response(question):
    try:
        response = requests.get(
            f"{base_url}/query",
            params={"question": question, "temperature": 0.7, "n_docs": 10},
            headers={"accept": "application/json"},
        )

        if response.status_code == 200:
            data = response.text
            return data
        else:
            st.session_state.history.append(
                {
                    "error": f"Failed to get response, status code: {response.status_code}"
                }
            )
            return None

    except Exception as e:
        st.session_state.history.append({"error": f"An error occurred: {str(e)}"})


# Now, the rest of the app follows
st.title("Chat with AI")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

# File upload section
uploaded_file = st.file_uploader(
    "Browse and select a PDF file:", type=["pdf"], key="file_uploader"
)
submit_button = st.button(label="Upload File", key="upload_button")
reset_upload_button = st.button(
    label="Reset Upload", key="reset_upload_button"
)  # Add a reset button

# Attempt to upload the file if the submit button is clicked and the file is selected
if submit_button and uploaded_file is not None and not st.session_state.file_uploaded:
    files = {"file": (uploaded_file.name, uploaded_file.read(), "application/pdf")}

    try:
        response = requests.post(
            f"{base_url}/upload?chunk_size=200",
            files=files,
            headers={"accept": "application/json"},
        )

        if response.status_code == 200:
            st.success("File uploaded successfully.")
            st.session_state.file_uploaded = (
                True  # Set the flag to True after successful upload
            )
        else:
            st.error(f"Failed to upload file, status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred while uploading the file: {str(e)}")

# Reset the upload state if the reset button is clicked
if reset_upload_button:
    st.session_state.file_uploaded = False
    st.info("Upload state reset.")

prompt = st.chat_input("Your question:")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    ai_response = get_ai_response(prompt)

    if ai_response:
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
