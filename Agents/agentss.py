import os
from dotenv import load_dotenv


load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if groq_api_key:
    from llama_index.llms.groq import Groq
    from llama_index.core.agent.workflow import FunctionAgent

    def multiply(a: float, b: float) -> float:
        """Multiply two numbers and return the product"""
        return a * b

    def add(a: float, b: float) -> float:
        """Add two numbers and return the sum"""
        return a + b

    llm = Groq(model="llama3-70b-8192", api_key=groq_api_key)

    workflow = FunctionAgent(
        tools=[multiply, add],
        llm=llm,
        system_prompt="You are an agent that can perform basic mathematical operations using tools.",
    )

    async def main():
        response = await workflow.run(user_msg="What is 20+(2*4)?")
        print(response)

    if __name__ == "__main__":
        import asyncio
        try:
            asyncio.run(main())
        except RuntimeError:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
else:
    print("GROQ_API key not found.")

    