from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from huggingface_hub import InferenceClient
import Secrets

@dataclass
class AgentRole:
    name: str
    description: str
    capabilities: List[str]
    constraints: List[str]

@dataclass
class Tool:
    name: str
    description: str
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        pass

class WebSearchTool(Tool):
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information about a given query"
        )
    
    def execute(self, query: str) -> str:
        # Simulate web search for demo purposes
        return f"Found information about: {query}"

class LLMEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key      
        self.client = InferenceClient(
            model="meta-llama/Llama-3.2-3B-Instruct",
            token=self.api_key
        )
    
    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        try:
            # Format prompt for Llama Instruct
            formatted_prompt = f"""<s>[INST] {prompt} [/INST]"""
            
            response = self.client.text_generation(
                formatted_prompt,
                max_new_tokens=max_tokens,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.1,
            )
            
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Error generating response"

class Agent:
    def __init__(
        self,
        name: str,
        role: AgentRole,
        tools: List[Tool],
        llm_engine: LLMEngine
    ):
        self.name = name
        self.role = role
        self.tools = {tool.name: tool for tool in tools}
        self.llm_engine = llm_engine
        self.conversation_history = []

    def think(self, task: str) -> Dict[str, Any]:
        """Analyze the task and determine the best course of action."""
        prompt = self._create_thinking_prompt(task)
        response = self.llm_engine.generate(prompt)
        return self._parse_thinking_response(response)

    def act(self, plan: Dict[str, Any]) -> Any:
        """Execute the plan created by think()"""
        results = []
        for step in plan['steps']:
            if step['tool'] in self.tools:
                tool = self.tools[step['tool']]
                result = tool.execute(**step['parameters'])
                results.append(result)
        return results

    def run(self, task: str) -> str:
        """Main execution loop of the agent"""
        self.conversation_history.append({"role": "user", "content": task})
        
        # Generate initial understanding
        understanding_prompt = f"""
        Given this task: "{task}"
        Provide a brief analysis of what needs to be done.
        """
        understanding = self.llm_engine.generate(understanding_prompt)
        print(understanding)
        
        # Create and execute plan
        plan = self.think(task)
        print(plan)
        results = self.act(plan)
        print(results)
        
        # Formulate final response
        response_prompt = f"""
        Based on these results: {results}
        And your understanding: {understanding}
        Provide a comprehensive response to the original task: "{task}"
        """
        final_response = self.llm_engine.generate(response_prompt)
        
        self.conversation_history.append({"role": "assistant", "content": final_response})
        return final_response

    def _create_thinking_prompt(self, task: str) -> str:
        return f"""
        Role: {self.role.name}
        Description: {self.role.description}
        
        Available Tools:
        {self._format_tools()}
        
        Task: {task}
        
        Create a plan with the following structure:
        {{
            "steps": [
                {{"tool": "tool_name", "parameters": {{"param_name": "value"}}}}
            ]
        }}
        """

    def _format_tools(self) -> str:
        return "\n".join([
            f"- {name}: {tool.description}"
            for name, tool in self.tools.items()
        ])

    def _parse_thinking_response(self, response: str) -> Dict[str, Any]:
        # Simplified parsing for demo purposes
        return {
            "steps": [
                {"tool": "web_search", "parameters": {"query": "sample query"}}
            ]
        }


def main():
    llm = LLMEngine(api_key=Secrets.HF_ACCESS_TOKEN) 
    
    # Create a role
    role = AgentRole(
        name="Research Assistant",
        description="I help users find and analyze information",
        capabilities=["Web searching", "Information synthesis"],
        constraints=["Only uses verified sources"]
    )
    
    # Create tools
    tools = []
    
    # Create the agent
    agent = Agent(
        name="ResearchBot",
        role=role,
        tools=tools,
        llm_engine=llm
    )
    
    # Test the agent
    query = "Why is America racist?"
    print(f"\nQuery: {query}")
    print("\nGenerating response...")
    response = agent.run(query)
    print(f"\nResponse: {response}")

if __name__ == "__main__":
    main()