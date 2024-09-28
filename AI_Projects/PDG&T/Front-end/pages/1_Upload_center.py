import streamlit as st
from api_calls import ApiCalls

st.header("Product Description Generator")

# Display Uploaded Files
def display_stored_files():
    with st.spinner("Loading uploaded files ..."):
        data: ApiCalls = ApiCalls().get_uploaded_files()
        if data:
            # Display data in table
            st.table(data)
        else:
            st.info("Files not found")


st.sidebar.info("Files are required to proceed!")
user_uploaded_files:            list | None  = st.sidebar.file_uploader("Upload Your files", accept_multiple_files=True)


# Inform User about ignoring image files and remove them from uploaded files
for file in user_uploaded_files:
    if file.type.startswith(("image", "audio", "video")):
        st.sidebar.info(f"Ignoring file named '{file.name}' as {file.type} files are not supported for now. To Upgrade it, Please contact at huzaifatahir332@gmail.com ")
        user_uploaded_files.remove(file)
        print(f"{file.type} file has been removed!")


# user should fill all fields
if user_uploaded_files:
    if st.sidebar.button("Save"):
        ApiCalls().upload_files(user_uploaded_files)


delete_all_button = st.button("Delete all")
if delete_all_button:
    ApiCalls().delete_all_files()


display_stored_files()