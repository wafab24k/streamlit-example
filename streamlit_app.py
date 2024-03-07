import openai
import os
import sys

openai.api_key = os.environ['OPENAI_API_KEY']


client = openai.OpenAI()



def get_completion(prompt, model="gpt-3.5-turbo"):
  messages = [{"role": "user", "content": prompt}]
  response =  client.chat.completions.create(
      model=model,
      messages=messages,
      temperature=0, 
  )
  return response.choices[0].message.content

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
  response =  client.chat.completions.create(
      model=model,
      messages=messages,
      temperature=temperature, 
  )

  return response.choices[0].message.content



def collect_messages(_):
  prompt = inp.value_input
  inp.value = ''
  context.append({'role':'user', 'content':f"{prompt}"})
  response = get_completion_from_messages(context) 
  context.append({'role':'assistant', 'content':f"{response}"})
  panels.append(
    pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
  panels.append(
    pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style=         {'background-color': '#F6F6F6'})))

  return pn.Column(*panels)


import panel as pn  # GUI
pn.extension()

panels = [] # collect display 

context = [ {'role':'system', 'content':"""
You are an AI assistant OrderBotf, an automated service to collect orders for supermarket. \
You first greet the customer, then collects the order, \
Ask if he prefer a specific brand for each canned and non fresh food, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
Once you collect the entire order, tell him that you will search for the lowest price across the available supermarkets. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, quantities and sizes to uniquely \
identify the item from the store.\
You respond in a short, very conversational friendly style. \
The shop includes \

Milk  \
Water  \
butter   \
Bakery \
Toast bread \
Vegetables & fruits \
apples \
Tomatos  \
mushrooms  \
Banana \
Meat \
Dairy & Eggs \
Nadec Mixed Blue Berry Greek Yoghurt  \
Saha Vitamin D Egg 30 Pieces \
peppers \
Drinks: \
coke \
sprite \
bottled water \
"""} ]  # accumulate messages


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)
pn.serve(dashboard, allow_websocket_origin=['dd626c76-125e-4892-b922-afcedf0d1bea-00-3s8b98slscpeg.sisko.replit.dev:3000'])
