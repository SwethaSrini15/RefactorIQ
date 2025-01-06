from crewai import Agent, Task, Crew, Process
from typing import List
from agents.junior_agent import JuniorAgent

class SeniorAgent:
    def __init__(self, language: str, files: List[str]):
        self.language = language
        self.files = files
        self.senior_agent = Agent(
            role=f'Senior {self.language} Developer',
            goal=(
                f"""Oversee the analysis of {self.language} code files, ensuring:
        
                • Thorough coverage of code structure, functionality, and adherence to coding standards.
                • Collaboration with Junior Agents to produce detailed findings.
                • Creation of consolidated, high-quality reports based on Junior outputs."""
            ),
            backstory=(
                f"""An experienced {self.language} developer with strong expertise in code review and analysis, 
                responsible for mentoring Junior Agents and maintaining high-quality deliverables."""
            ),
            llm="openrouter/openai/gpt-4o-mini-2024-07-18",
        )

    def create_junior_agents(self) -> List[JuniorAgent]:
        junior_agents = []
        chunks = [self.files[i:i + 5] for i in range(0, len(self.files), 5)]
        for idx, chunk in enumerate(chunks, start=1):
            junior_agent = JuniorAgent(self.language, chunk, idx)
            junior_agents.append(junior_agent)
        return junior_agents

    async def execute(self) -> str:
        junior_agents = self.create_junior_agents()
        junior_tasks = []
        
        for agent in junior_agents:
            junior_tasks.extend(agent.create_tasks())
        
        # Create a single crew with junior and senior agents
        agents = [agent.junior_agent for agent in junior_agents] + [self.senior_agent]
        process_tasks = junior_tasks + [
            Task(
                description=(
                    f"As a Senior {self.language} Developer, analyze Junior Agents' outputs and provide a consolidated report."
                ),
                expected_output="A cohesive summary of the project integrating all Junior Agents' findings.",
                agent=self.senior_agent,
                
            )
        ]

        crew = Crew(
            agents=agents,
            tasks=process_tasks,
            process=Process.sequential,
        )
        # Asynchronously kickoff the unified crew
        outputs = await crew.kickoff_async()

        # Consolidate junior and senior outputs
        summary = "\n".join(str(output.content) if hasattr(output, 'content') else str(output) for output in outputs)
        return summary
