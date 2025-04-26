#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install langchain langchain-community langgraph beautifulsoup4 requests langchain-openai')

import os
import requests
from bs4 import BeautifulSoup
from langchain.agents import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI  # Updated import
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
import ipywidgets as widgets
from IPython.display import display

os.environ["TAVILY_API_KEY"] = "Your key"  # Replace with your actual Tavily API key
os.environ["OPENAI_API_KEY"] = "Your API key"  # Replace with your actual OpenAI API key

search_tool = Tool.from_function(
    name="TavilySearch",
    func=TavilySearchResults().run,
    description="Useful for answering questions about current events or factual information from the web."
)

class ResearchState(TypedDict):
    query: str
    search_results: Optional[str]
    final_answer: Optional[str]

# Define LangGraph Nodes
def initial_prompt_node(state):
    return {"query": state["query"]}

def search_node(state):
    query = state["query"]
    results = search_tool.run(query)
    return {"search_results": results}

def drafting_node(state):
    docs = state["search_results"]
    prompt = f"Based on the following research, generate a concise and informative answer:\n{docs}"
    response = ChatOpenAI(temperature=0.2).invoke(prompt)
    return {"final_answer": response.content}

# Build the LangGraph Workflow
builder = StateGraph(ResearchState)
builder.add_node("InitialPrompt", initial_prompt_node)
builder.add_node("ResearchAgent", search_node)
builder.add_node("DraftingAgent", drafting_node)

builder.set_entry_point("InitialPrompt")
builder.add_edge("InitialPrompt", "ResearchAgent")
builder.add_edge("ResearchAgent", "DraftingAgent")
builder.add_edge("DraftingAgent", END)

graph = builder.compile()

query_input = widgets.Text(
    description='Query:',
    placeholder='e.g. What are the latest trends in climate change policy?'
)

run_button = widgets.Button(description='Run Deep Research')
output_area = widgets.Output()

def on_button_click(b):
    with output_area:
        output_area.clear_output()
        query = query_input.value
        if query:
            state = {"query": query, "search_results": None, "final_answer": None}
            try:
                result = graph.invoke(state)
                print("Final Answer:")
                print(result['final_answer'])
                print("\n Research Data:")
                print(result['search_results'])
            except Exception as e:
                print(f"An error occurred: {e}")

run_button.on_click(on_button_click)

display(query_input, run_button, output_area)

