# AI-Powered Code Analysis and Documentation System

This project is an advanced AI-driven system for comprehensive code analysis and technical documentation generation.

The system employs a hierarchical structure of AI agents to analyze and document software projects. It consists of Junior Agents, Senior Agents, and a Super Senior Agent, each with specific roles in the analysis process. The system is designed to handle multi-language projects, providing in-depth insights into code structure, quality, and architecture.

Key features include:
- Automated code analysis for multiple programming languages
- Hierarchical agent structure for comprehensive review
- Generation of detailed technical documentation
- Creation of architecture and data flow diagrams using Mermaid
- Identification of potential bugs, vulnerabilities, and areas for improvement
- Evaluation of code quality, maintainability, and scalability
- Synthesis of findings into actionable insights

## Repository Structure

```
.
├── agents
│   ├── __init__.py
│   ├── junior_agent.py
│   ├── senior_agent.py
│   └── super_senior_agent.py
├── app.py
└── utils
    ├── __init__.py
    ├── analysis_utils.py
    ├── file_utils.py
    └── languages.py
```

### Key Files:
- `app.py`: The main entry point of the application
- `agents/super_senior_agent.py`: Implements the SuperSeniorAgent class, which orchestrates the entire analysis process
- `agents/senior_agent.py`: Defines the SeniorAgent class, responsible for managing JuniorAgents and consolidating their outputs
- `agents/junior_agent.py`: Contains the JuniorAgent class, which performs detailed analysis on specific code files
- `utils/analysis_utils.py`: Provides utility functions for language detection and folder analysis
- `utils/file_utils.py`: Offers functions for zip file extraction and directory cleanup
- `utils/languages.py`: Contains a dictionary mapping file extensions to programming languages

## Usage Instructions

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone <repository_url>
   cd <repository_name>
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   LANGTRACE_API_KEY=your_langtrace_api_key
   ```

### Running the Application

1. Prepare your code for analysis by zipping it into a file named `cregentic-main.zip` in the project root.

2. Run the main application:
   ```
   python app.py
   ```

3. The system will analyze the code and generate a technical documentation file named `technical_documentation.docx` in the project root.

### Configuration Options

- To modify the language detection logic, update the `LANGUAGE_DICTIONARY` in `utils/languages.py`.
- Adjust the number of files processed by each JuniorAgent by modifying the chunk size in `agents/senior_agent.py`.

### Common Use Cases

1. Analyzing a new project:
   - Zip the project files into `cregentic-main.zip`
   - Run `python app.py`
   - Review the generated `technical_documentation.docx`

2. Customizing agent behavior:
   - Modify the agent roles, goals, and backstories in the respective agent files
   - Adjust the LLM models used by updating the `llm` parameter in the Agent initialization

### Troubleshooting

1. Issue: No code files found in the zip file
   - Error message: "No code files found."
   - Solution: Ensure that the zip file contains valid code files and is named `cregentic-main.zip`

2. Issue: LangTrace API key not recognized
   - Error message: "LangTrace API key not found or invalid"
   - Solution: Verify that the `LANGTRACE_API_KEY` is correctly set in the `.env` file

3. Issue: Memory errors when processing large projects
   - Error message: "MemoryError" or system becomes unresponsive
   - Solution: 
     - Increase the chunk size in `agents/senior_agent.py` to process fewer files per JuniorAgent
     - Adjust the `buffer_size` in `agents/junior_agent.py` if dealing with large individual files

### Debugging

To enable verbose logging:
1. Open `app.py`
2. Uncomment the line `# litellm.set_verbose=True`

Log files are typically stored in the `logs` directory (create if not present) in the project root.

### Performance Optimization

- Monitor CPU and memory usage during execution
- If processing is slow, consider increasing the `max_workers` parameter in the `ThreadPoolExecutor` in `agents/junior_agent.py`
- For large projects, consider implementing batching in the `SuperSeniorAgent` to process subsets of the project in stages

## Data Flow

The data flow in this application follows these steps:

1. The user provides a zip file containing the code to be analyzed.
2. The SuperSeniorAgent extracts the zip file and analyzes the folder structure.
3. SeniorAgents are created for each detected programming language.
4. Each SeniorAgent creates multiple JuniorAgents to analyze specific subsets of files.
5. JuniorAgents perform detailed analysis on their assigned files.
6. SeniorAgents consolidate the outputs from their JuniorAgents.
7. The SuperSeniorAgent synthesizes all findings into a final technical documentation.

```
[User] -> [Zip File] -> [SuperSeniorAgent] -> [SeniorAgents] -> [JuniorAgents]
                                                    ^                |
                                                    |                |
                                                    +----------------+
                                                    (Consolidation)
         [Technical Documentation] <- [SuperSeniorAgent] <- [SeniorAgents]
```

Note: The system uses asynchronous execution and threading to optimize performance when dealing with multiple files and agents.