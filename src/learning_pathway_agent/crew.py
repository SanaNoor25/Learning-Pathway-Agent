import os


from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.learning_pathway_agent.tools.mcp_tools import (
    get_role_data,
    get_learning_resources,
    web_search
)





@CrewBase
class LearningPathwayAgentCrew:
    """LearningPathwayAgent crew"""

    
    @agent
    def skill_gap_analyst(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["skill_gap_analyst"],
            
            
            tools=[get_role_data],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openrouter/mistralai/ministral-8b-2512",
                api_key=os.getenv("OPENROUTER_API_KEY_1", "").strip(),
                max_tokens=2000,
                temperature=0.3
                
            ),
            
        )
        
    
    @agent
    def learning_path_planner(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["learning_path_planner"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openrouter/mistralai/ministral-8b-2512",
                api_key=os.getenv("OPENROUTER_API_KEY_1", "").strip(),
                max_tokens=2000,
                temperature=0.3
                
            ),
            
        )
        
    
    @agent
    def resource_recommendation_agent(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["resource_recommendation_agent"],
            
            
            tools=[get_learning_resources, web_search],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openrouter/mistralai/ministral-8b-2512",
                api_key=os.getenv("OPENROUTER_API_KEY_1", "").strip(),
                max_tokens=2000,
                temperature=0.3
                
            ),
            
        )
        
    
    @agent
    def progress_tracking_agent(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["progress_tracking_agent"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openrouter/mistralai/ministral-8b-2512",
                api_key=os.getenv("OPENROUTER_API_KEY_1", "").strip(),
                max_tokens=2000,
                temperature=0.3
                
            ),
            
        )
        
    
    @agent
    def adaptive_recommendation_agent(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["adaptive_recommendation_agent"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openrouter/mistralai/ministral-8b-2512",
                api_key=os.getenv("OPENROUTER_API_KEY_2", "").strip(),
                max_tokens=3000,
                temperature=0.3
                
            ),
            
        )
  
    

    
    @task
    def retrieve_target_role_requirements(self) -> Task:
        return Task(
            config=self.tasks_config["retrieve_target_role_requirements"],
            markdown=False,
            
            
        )
    
    @task
    def analyze_student_profile(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_student_profile"],
            markdown=False,
            
            
        )
    
    @task
    def process_interview_feedback(self) -> Task:
        return Task(
            config=self.tasks_config["process_interview_feedback"],
            markdown=False,
            
            
        )
    
    @task
    def generate_skill_gap_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["generate_skill_gap_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def build_learning_roadmap(self) -> Task:
        return Task(
            config=self.tasks_config["build_learning_roadmap"],
            markdown=False,
            
            
        )
    
    @task
    def curate_learning_resources(self) -> Task:
        return Task(
            config=self.tasks_config["curate_learning_resources"],
            markdown=False,
            
            
        )
    
    @task
    def track_and_update_progress(self) -> Task:
        return Task(
            config=self.tasks_config["track_and_update_progress"],
            markdown=False,
            
            
        )
    
    @task
    def generate_adaptive_learning_plan(self) -> Task:
        return Task(
            config=self.tasks_config["generate_adaptive_learning_plan"],
            markdown=True,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the LearningPathwayAgent crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

            chat_llm=LLM(
                model="openrouter/openai/gpt-4o-mini",
                api_key=os.getenv("OPENROUTER_API_KEY_1", "").strip(),
                max_tokens=1500,
                ),
        )

