import os
import asyncio
from dotenv import load_dotenv
from agents.super_senior_agent import SuperSeniorAgent
from langtrace_python_sdk import langtrace, inject_additional_attributes
import litellm

# Load environment variables
load_dotenv()
litellm.set_verbose=True
# # # Initialize LangTrace
langtrace.init(
    api_key=os.getenv("LANGTRACE_API_KEY"),
)

async def main():
    try:
        super_senior_agent = SuperSeniorAgent()
        zip_file_path = "free-react-tailwind-admin-dashboard-main.zip"
        await super_senior_agent.execute(zip_file_path)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())