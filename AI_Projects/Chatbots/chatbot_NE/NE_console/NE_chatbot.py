import openai

with open("openai_credentials.txt") as f:
    OPENAI_API_KEY = f.read()
openai.api_key = OPENAI_API_KEY

def get_complition(message, model="gpt-3.5-turbo"):
  response = openai.ChatCompletion.create(
      model = model,
      messages=message,
      temperature=0
  )
  return response.choices[0].message.content


def save_in_file(role ,data):
    with open("context.text", "a") as f:
        f.write(f"\n{role}: {data}")



messages=[{"role":"system", "content":"""
            Your name is Huzaifa Tahir
            You are a Network Engineer by profession.
            You only response on the network related user queries.
            Must be specify with user query. don't provide any extra information.
            Response no longer than 30 words.
            Do not give extra responses. 
            Must be specify with user query.
            You only response on the network related queries.
            If user ask any query that is not the networking domain. don't provide that information
            """}]



while True:
    user_query = input('user: ')
    if user_query == "quit":
        print(len(messages))
        print(messages)
        break
    save_in_file("user" ,user_query)
    messages.append({"role":"user", "content":f"{user_query}"})
    bot_reply = get_complition(messages)
    print(f"BOT: {bot_reply}")
    save_in_file("assistant", bot_reply)
    messages.append({"role":"assistant", "content":f"{bot_reply}"})
