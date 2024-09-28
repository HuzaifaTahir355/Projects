import streamlit as st
from api_calls import ApiCalls


st.header("Product Description Generator")

# get languages from user
languages: list[str] = st.sidebar.multiselect("Select Languages to translate", ["French", "Arabic", "Spanish", "Urdu"])


# both input should contain values
if languages:
    if st.sidebar.button("Proceed"):
        with st.spinner("Working on uploaded Documents..."):   
            data: ApiCalls = ApiCalls().get_product_description_and_image(languages)
            if not data:
                # st.error("Something went wrong! Please contact at huzaifatahir332@gmail.com")
                st.error("No data Found! Please upload the files first.")
            elif "Error" in data:
                st.error(str.removeprefix(data, "Error"))
            else:
                num_of_products: int = len(data)
                st.write(f"### Total {num_of_products} {'products are listed' if num_of_products > 1 else 'product is listed' }")
                for i, product in enumerate(data):
                    st.write(f"#### {i+1}) ***{product['product_name']}***")
                    for language, description in product['description'].items():
                        st.write(f"**{language}**")
                        st.write(description)
else:
    st.info("At least one language is required!")
