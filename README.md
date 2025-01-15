# RefactorIQ Installation and Usage Guide

## Prerequisites
- Python 3.7 or higher
- pip package manager

## Installation Steps

1. Install md2docx and other required packages:
```bash
pip install md2docx crewai openrouter-py python-dotenv
```

2. Set up your OpenRouter API key in `.env`:
```
OPENROUTER_API_KEY=your_api_key_here
```

## Usage

1. Place your code zip file in the project directory.

2. Run the analysis:
```python
import asyncio
from agents.super_senior_agent import SuperSeniorAgent

async def main():
    agent = SuperSeniorAgent()
    await agent.execute("your_code.zip")

if __name__ == "__main__":
    asyncio.run(main())
```

The script will:
1. Extract and analyze your code
2. Generate a detailed technical analysis
3. Create a formatted Word document named "Final technical document.docx"

## Output

The generated document will include:
- Architecture analysis
- Code quality assessment
- Data flow diagrams (using Mermaid syntax)
- Technical debt identification
- Improvement recommendations

The output is first generated in Markdown format for clean formatting, then automatically converted to a properly formatted Word document using md2docx.
