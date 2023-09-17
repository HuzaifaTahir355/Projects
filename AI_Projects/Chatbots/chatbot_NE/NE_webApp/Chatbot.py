import streamlit as st
import openai

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY


with st.sidebar:
    st.header("Huzaifa Tahir")
    st.write("Network Engineer")
    st.divider()
    if st.button("Remove Previous chat"):
        with open("context.txt", "w") as f:
            f.flush()


def get_complition(message, model="gpt-3.5-turbo"):
  response = openai.ChatCompletion.create(
      model = model,
      messages=message,
      temperature=0
  )
  return response.choices[0].message.content


def save_in_file(role ,data):
    with open("context.txt", "a") as f:
        f.write(f"\n{data}")

def read_file():
    with open("context.txt", "r") as f:
        file_data = f.read().splitlines()
        for i in range(1, len(file_data)):
            if i % 2 == 0:
                with st.chat_message(name="assistant", avatar="assistant"):
                    st.write(file_data[i])
            else:
                with st.chat_message(name="user", avatar="user"):
                    st.write(file_data[i])

messages=[{"role":"system", "content":"""
            Your name is Huzaifa Tahir
            You are a Network Engineer by profession.
            Huzaifa Tahir have done Certification like CCNA, CCNP, HCIA, HCIP.
            Huzaifa Tahir is a national Finalist in Huawei ICT compitition 2022-23.
            You only response on the network related user queries.
            Must be specify with user query. don't provide any extra information.
            Response no longer than 50 words.
            Do not give extra responses. 
            Must be specify with user query.
            You only response on the network related queries.
            If user ask any query that is not the networking domain slightly move user to networking.
            """}]


user_query = st.chat_input("Your message here")
if user_query:
    save_in_file("user" ,user_query)
    messages.append({"role":"user", "content":f"{user_query}"})
    bot_reply = get_complition(messages)
    save_in_file("assistant", bot_reply)
    messages.append({"role":"assistant", "content":f"{bot_reply}"})
read_file()