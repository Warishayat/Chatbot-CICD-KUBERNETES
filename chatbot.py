from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages,BaseMessage
from typing import TypedDict,Annotated,List,Literal
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel,Field
from dotenv import load_dotenv
import os

load_dotenv()
chk_pointer = InMemorySaver()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

Model = ChatGroq(
    model_name="openai/gpt-oss-20b",
    groq_api_key=GROQ_API_KEY,
    temperature=0.2
)




class ChatbotState(TypedDict):
  messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state: ChatbotState):
  msg = state["messages"]
  response = Model.invoke(msg)

  return {
      "messages": [response]
  }

graphh = StateGraph(ChatbotState)
graphh.add_node("chatnode",chat_node)
graphh.add_edge(START,"chatnode")
graphh.add_edge("chatnode",END)



chatbot=graphh.compile(checkpointer=chk_pointer)

config = {
    "configurable": {
        "thread_id": "waris"
    }
}

