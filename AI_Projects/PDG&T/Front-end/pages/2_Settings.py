import streamlit as st
from api_calls import ApiCalls


st.header("⚙️ Settings")


last_saved_settings = ApiCalls().get_saved_settings()

user_selected_chunk_size:      int  | None  = int(st.number_input("Chunk Size", 
                                                                  value=last_saved_settings[0]["chunk_size"]))
                                                                #   value=ApiCalls().get_default_chunk_size()))
user_selected_embedding_model: str  | None  = st.selectbox("Select Embedding Model", 
                                                           options=ApiCalls().get_available_embedding_models(user_selected_chunk_size),
                                                           index=None,
                                                           placeholder=last_saved_settings[0]["embedding_model"])
user_selected_vector_store:    str  | None  = st.selectbox("Select Vector Store/DB", 
                                                           options=ApiCalls().get_available_vector_stores(), 
                                                           index=None,
                                                           placeholder=last_saved_settings[0]["vector_store"])
# get llm from user
user_selected_llm: list[str] = st.selectbox("Select Model", 
                                            options=ApiCalls().get_available_llms(), 
                                            index=None,
                                            placeholder=last_saved_settings[0]["selected_llm"])
# image generation check
image_required: bool = st.checkbox("AI Generated Image of each product is Required", value=False, disabled=True)

if user_selected_chunk_size and user_selected_embedding_model and user_selected_vector_store and user_selected_llm:
    if st.button("Save"):
        ApiCalls().set_values_of_settings(user_selected_chunk_size, 
                                          user_selected_embedding_model,
                                          user_selected_vector_store, 
                                          image_required,
                                          user_selected_llm)
else:
    st.info("All fields are required to proceed!")