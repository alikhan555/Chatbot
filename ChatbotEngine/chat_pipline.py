from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


class Chat:
    def __init__(self):
        self.workflow = self.generate_graph()
        pass

    def chat_node(self, state: ChatState):
        messages = state["messages"]
        llm = init_chat_model(model="gpt-5-nano", model_provider="openai")
        response = llm.invoke(messages)
        return {"messages": [response]}

    def generate_graph(self):
        checkpointer = MemorySaver()
        graph = StateGraph(ChatState)
        graph.add_node("chat_node", self.chat_node)
        graph.add_edge(START, "chat_node")
        graph.add_edge("chat_node", END)
        workflow = graph.compile(checkpointer=checkpointer)
        return workflow

    def send_message(self, message, thread_id):
        initial_state = {"messages": [HumanMessage(message)]}
        config = {"configurable": {"thread_id": thread_id}}
        response = self.workflow.invoke(initial_state, config=config)
        return response
