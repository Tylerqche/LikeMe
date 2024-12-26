from typing import List, Dict, Any
from dataclasses import dataclass
import agent_tools
import Secrets
from llm_engine import LLMEngine
from agents import AgentRole, Agent

def main():
    llm = LLMEngine(api_key=Secrets.HF_ACCESS_TOKEN) 
    
    # Create Tools
    tools = {
        "web_search": agent_tools.WebSearchTool(),
        "parse_pdf": agent_tools.PDFParserTool()
    }

    # Create Agent Descriptions
    technical_recruiter = AgentRole(
        name="Technical Recruiter",
        description="You are a highly skilled technical recruiter specializing in sourcing and evaluating  top-tier talent for engineering and technical roles at innovative companies.",
        capabilities=["web_search", "parse_pdf"],
    )
    
    agent = Agent(
        name="Main",
        role=technical_recruiter,
        tools=tools,
        llm_engine=llm
    )
    
    # Test the agent
    query = "What color is the sky?"
    response = agent.run(query)
    print(f"\nResponse: {response}")

if __name__ == "__main__":
    main()