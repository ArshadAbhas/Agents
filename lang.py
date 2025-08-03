from typing import Annotated
from dotenv import load_dotenv
import os

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)



load_dotenv()


model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")



def chatbot(state: State):
    return {"messages": [model.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()
user_input = input("You: ")

# Start state with the user's message
initial_state = {"messages": [user_input]}

# Run the graph with the user's message
final_state = graph.invoke(initial_state)

# Get the response
bot_reply = final_state["messages"][0]

print("Bot:", bot_reply)
