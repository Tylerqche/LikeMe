import agent_tools
from llm_engine import LLMEngine
from agents import AgentRole, Agent

# Create Tools
tools = {
    "web_search": agent_tools.WebSearchTool(),
    "parse_pdf": agent_tools.PDFParserTool(),
    "web_parser": agent_tools.WebParserTool()
}

# Coordinator Agent
coordinator_role = AgentRole(
    name="Coordinator Agent",
    description="You are responsible for overseeing the entire resume and cover letter optimization process. You delegate tasks to other agents, ensure they have the necessary information, and verify outputs for quality and alignment with the job description and company goals.",
    capabilities=["web_search", "parse_pdf", "web_parser"],
)

# Resume Analyst Agent
resume_analyst_role = AgentRole(
    name="Resume Analyst",
    description="You are an expert in reviewing resumes for ATS optimization and content enhancement. Your task is to analyze resumes, suggest improvements to match job descriptions, and identify gaps in skills or experience that need to be addressed.",
    capabilities=["web_search", "parse_pdf", "web_parser"],
)

# Job Description Analyst Agent
job_description_analyst_role = AgentRole(
    name="Job Description Analyst",
    description="You specialize in analyzing job descriptions to extract key requirements, skills, and company values. Your goal is to ensure resumes and cover letters align with these elements and improve the candidate's chances of selection.",
    capabilities=["web_search", "parse_pdf", "web_parser"],
)

# Cover Letter Writer Agent
cover_letter_writer_role = AgentRole(
    name="Cover Letter Writer",
    description="You are a skilled writer who creates tailored, professional, and compelling cover letters that align with the job description and highlight the candidate's strengths and achievements.",
    capabilities=["web_search", "parse_pdf", "web_parser"],
)

# Resume Writer Agent
resume_writer_role = AgentRole(
    name="Resume Writer",
    description="You are responsible for drafting and editing resumes to ensure they are ATS-friendly and highlight the candidate's relevant skills, experiences, and achievements for the target job.",
    capabilities=["web_search", "parse_pdf", "web_parser"],
)

# Technical Reader Agent
technical_reader_role = AgentRole(
    name="Technical Reader",
    description="You are an expert in analyzing input materials such as resumes, job descriptions, and company details. Your role is to extract and summarize key information to guide other agents in the optimization process.",
    capabilities=["web_search", "parse_pdf", "web_parser"],
)

# Create agents
coordinator = Agent(name="Coordinator", role=coordinator_role, tools=tools, llm_engine=LLMEngine),
resume_analyst = Agent(name="Resume Analyst", role=resume_analyst_role, tools=tools, llm_engine=LLMEngine),
job_description_analyst = Agent(name="Job Description Analyst", role=job_description_analyst_role, tools=tools, llm_engine=LLMEngine),
cover_letter_writer = Agent(name="Cover Letter Writer", role=cover_letter_writer_role, tools=tools, llm_engine=LLMEngine),
resume_writer = Agent(name="Resume Writer", role=resume_writer_role, tools=tools, llm_engine=LLMEngine),
technical_reader = Agent(name="Technical Reader", role=technical_reader_role, tools=tools, llm_engine=LLMEngine)