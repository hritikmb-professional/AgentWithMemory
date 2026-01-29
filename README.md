# Agent with Memory and Tool

AI-powered Flask API featuring two specialized research agents with persistent memory and real-time web search capabilities.

## Features

**Live Market Researcher Agent**
- Real-time web search via Tavily API
- Analyzes market trends and current events
- Concise summarization of findings

**Analyst Agent**
- Dual capabilities: web search + Python code execution
- Data analysis and calculations
- Combined research and computational tasks

**Persistent Memory**
- SQLite session storage across conversations
- Context retention for follow-up queries
- Conversation history tracking

## Tech Stack

- **Framework:** Flask REST API
- **LLM:** GPT-4.1-mini (OpenAI)
- **Tools:** Tavily Search, Code Interpreter
- **Memory:** SQLite session management
- **Library:** OpenAI Agents SDK

## API Endpoints

```bash
POST /ask/live
# Live market research with web search

POST /ask/analyst
# Analysis with search + code execution
```

## Setup

```bash
pip install openai python-dotenv flask requests agents
```

Create `.env`:
```
OPENAI_API_KEY=your_key
TAVILY_API_KEY=your_key
```

Run:
```bash
python a.py
```

## Usage

```bash
curl -X POST http://localhost:5000/ask/live \
  -H "Content-Type: application/json" \
  -d '{"question": "Latest Tesla stock news?"}'
```

Both agents maintain conversation context and can handle complex, multi-turn research queries with accurate, up-to-date information.
