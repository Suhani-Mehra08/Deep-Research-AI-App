
# Deep Research AI Agentic System

This project implements a Deep Research AI Agentic System using LangChain, LangGraph, and Tavily API.

## System Overview

- **Research Agent**: Gathers web data using Tavily API.
- **Answer Drafter Agent**: Summarizes the research into a report.
- **LangGraph**: Manages the interaction between agents.

## Requirements

- Python 3.10+
- OpenAI API Key
- Tavily API Key
- LangChain
- LangGraph
- Tavily Python SDK

## How to Run

1. Install dependencies: `pip install -r requirements.txt`
2. Add your API keys in `config.py`.
3. Run the agent system: `python deep_research_agent.py`
