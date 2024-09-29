from audio_recorder_streamlit import audio_recorder
from api_calls import ApiCalls
import streamlit as st

st.header("Speak & Seek Assistant")

web_url: str = st.text_input("URL of Website")
audio_bytes: bytes | None = audio_recorder(
    text="Click to Ask question",
    recording_color="red",
    neutral_color="white",
    icon_name="microphone-lines",
    icon_size="2x",
)

if web_url:
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        if st.button("Proceed"):
            # User query
            user_query: ApiCalls = ApiCalls().text_from_speech(audio_bytes)
            st.write(user_query)
            # convert text to Audio
            answer: str = ApiCalls().qa_from_url(web_url, user_query)
            st.write(answer)
            # convert text to Audio
            # answer = "Dr. Sheraz Naseer is the Head of AI Department, Prof. Dr. Javed Iqbal is a Healthcare SME, and Ayaz Qaiser is the CTO at Xeven Solutions."
            audio_data: ApiCalls = ApiCalls().text_to_speech(answer)
            st.audio(audio_data, format="audio/mpeg")  # Play the audio in Streamlit

else:
    st.error("URL is required")