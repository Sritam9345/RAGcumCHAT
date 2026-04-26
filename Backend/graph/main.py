from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal,Annotated
import operator
from langgraph.checkpoint.memory import InMemorySaver
from llm.model import model
from langchain_core.messages import HumanMessage,BaseMessage

class ChatState(TypedDict):
    
    messages: Annotated[list[str], operator.add]
    
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

def chat(state:ChatState):
    
    print(state['messages'])
    
    response = model.invoke(state['messages']).content
    
    return {'messages':[response]}
    
    


graph.add_node('chat',chat)

graph.add_edge(START,'chat')
graph.add_edge('chat',END)


workflow = graph.compile(checkpointer=checkpointer)

def graph_start(user_input,thread_id):
    
    config = {
    "configurable": {
        "thread_id": thread_id
    }
}
    
    response = workflow.invoke(
    {
        "messages": [user_input]
    },
    config=config
)
    print(response)
    
    return response
