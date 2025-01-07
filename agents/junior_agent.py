from crewai import Agent, Task
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

class JuniorAgent:
    def __init__(self, language: str, files: List[str], index: int):
        self.language = language
        self.files = files
        self.index = index
        self.junior_agent =  Agent(
            role=f'Junior {self.language} Developer {self.index}',
            goal=(
                f"""Conduct an in-depth analysis of assigned {self.language} code files, focusing on:

                • Documenting core functionalities and their interactions.
                • Identifying bugs, vulnerabilities, or inefficiencies, and proposing improvements.
                • Ensuring best practices in modularity, readability, and scalability.
                • Writing concise, actionable reports detailing findings and recommendations.
                • Creating initial drafts of architectural diagrams, data flows, and workflows for Senior Developer review.

                Maintain clear communication with the team to discuss observations, potential issues, and enhancements."""
            ),
            backstory=(
                f"""A detail-oriented, proactive Junior {self.language} Developer with a strong interest in improving code quality.
                This role involves analyzing specific sections of the project, spotting optimization opportunities, and 
                contributing foundational diagrams using Mermaid syntax. Working closely with Senior Developers, 
                the Junior Developer upholds project standards and provides valuable insights to strengthen the codebase."""
            ),
            llm="openrouter/google/gemini-flash-1.5",
            verbose= True,
            )

    def create_tasks(self) -> List[Task]:
        tasks = []
        code_contents = []
        
        def read_file(file_path):
            try:
                # Use binary mode and larger buffer size
                buffer_size = 4 * 1024 * 1024  # 4MB buffer
                with open(file_path, 'rb', buffering=buffer_size) as f:
                    return f.read().decode('utf-8', errors='ignore')
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")
                return None

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_file = {executor.submit(read_file, file_path): file_path for file_path in self.files}
            for future in as_completed(future_to_file):
                result = future.result()
                if result:
                    code_contents.append(result)

        if not code_contents:
            print(f"No code contents found for agent {self.junior_agent.role}")
            return tasks

        description = (
            f"As a Junior {self.language} Developer, analyze the following {self.language} code files within a larger project. "
            "Summarize how these files contribute to overall functionality and note any key issues or observations. "
            "Omit the full code and focus on core insights.\n\n"
            + "\n\n".join(code_contents)
        )
        expected_output = (
            f"A concise report summarizing the role of each {self.language} file in the project, "
            "highlighting critical findings, issues, and potential improvements."
        )
        task = Task(
            description=description,
            expected_output=expected_output,
            agent=self.junior_agent,
            async_execution=True
        )
        tasks.append(task)
        return tasks
