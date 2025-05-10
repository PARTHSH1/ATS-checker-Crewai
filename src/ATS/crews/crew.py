from crewai import Agent,Crew , Process,Task
from crewai.project import CrewBase,agent,crew,task
from crewai import LLM
from dotenv import load_dotenv
load_dotenv()
llm=LLM(model="groq/llama-3.3-70b-versatile")
@CrewBase
class ResumeCrew():
    """Resume crew"""
    @agent
    def content_matching_agent(self) -> Agent:  # Renamed to match the expected name
        return Agent(
            config=self.agents_config['content_matching_agent'],
            verbose=True,
            llm=llm
        )
    
    @agent
    def format_matching_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['format_matching_agent'],
            verbose=True,
            llm=llm
        )
    
    @agent 
    def section_specific_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['section_specific_agent'],
            verbose=True,
            llm=llm
        )
    
    @agent
    def overall_score_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['overall_score_agent'],
            verbose=True,
            llm=llm
        )
    
    @task
    def content_match_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_match_task'],
            # Don't reference the task itself in the context
            agent=self.content_matching_agent()  # Reference the agent directly
        )
    
    @task
    def format_match_task(self) -> Task:
        return Task(
            config=self.tasks_config['format_match_task'],
            agent=self.format_matching_agent()  # Reference the agent directly
        )
    
    @task
    def section_specific_task(self) -> Task:
        return Task(
            config=self.tasks_config['section_specific_task'],
            agent=self.section_specific_agent()  # Reference the agent directly
        )
    
    @task
    def combined_overall_score_task(self) -> Task:
        return Task(
            config=self.tasks_config['overall_score_task'],
            agent=self.overall_score_agent()  # Reference the agent directly
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            process=Process.sequential
        )