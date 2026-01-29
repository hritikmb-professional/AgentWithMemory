import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from IPython.display import display, Markdown
import json
from typing_extensions import TypedDict, Any
from agents import function_tool, SQLiteSession, Agent, Runner, FunctionTool, CodeInterpreterTool
from flask import Flask, request, jsonify

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

openai_client = OpenAI(api_key=openai_api_key)

def print_markdown(text: str):
    display(Markdown(text))

class TavilySearchParams(TypedDict):
    query: str
    max_results: int

@function_tool
def tavily_search(params: TavilySearchParams) -> str:
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": tavily_api_key,
        "query": params["query"],
        "max_results": params.get("max_results", 2),
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        results = response.json().get("results", [])
        summary = "\n".join([f"{i+1}. {r['title']}: {r['content']}" for i, r in enumerate(results)])
        return summary if summary else "No relevant results found."
    else:
        return f"Tavily API error: {response.status_code}"

session = SQLiteSession("live_researcher_practice")

live_researcher_agent = Agent(
    name="Live Market Researcher",
    instructions="""
CONTEXT:
You are a world-class market research assistant with access to real-time web search via the tavily_search tool.

INSTRUCTION:
- Analyze the user's question and determine if recent or real-time information is needed.
- If the question involves recent events, news, or product info, always call tavily_search.
- Summarize search results clearly and concisely, do not copy-paste.
- Always start your answer with: "According to a web search …"
""",
    model="gpt-4.1-mini",
    tools=[tavily_search],
)

code_interpreter = CodeInterpreterTool(
    tool_config={"type": "code_interpreter", "container": {"type": "auto"}}
)

analyst_agent = Agent(
    name="Analyst Agent",
    instructions="""
CONTEXT:
You are a world-class market research assistant with access to both real-time web search (via the tavily_search tool) and Python code execution (via the code_interpreter tool).

INSTRUCTION:
- Carefully analyze the user's question to determine whether it requires:
    - Recent or real-time information
    - Data analysis or calculations
    - Or both
- Use tavily_search for up-to-date facts.
- Use code_interpreter for calculations.
- Summarize findings clearly.
- When using search, begin with: "According to a web search …"
""",
    model="gpt-4.1-mini",
    tools=[tavily_search, code_interpreter],
)

app = Flask(__name__)

@app.route("/ask/live", methods=["POST"])
def ask_live():
    q = request.json["question"]
    run = Runner.run_sync(
        starting_agent=live_researcher_agent,
        input=q,
        session=session,
    )
    return jsonify({"answer": run.final_output})

@app.route("/ask/analyst", methods=["POST"])
def ask_analyst():
    q = request.json["question"]
    run = Runner.run_sync(
        starting_agent=analyst_agent,
        input=q,
        session=session,
    )
    return jsonify({"answer": run.final_output})

if __name__ == "__main__":
    app.run(debug=True)
