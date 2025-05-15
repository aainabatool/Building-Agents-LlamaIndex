import os
from dotenv import load_dotenv


load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if groq_api_key:
    from llama_index.llms.groq import Groq
    from llama_index.core.agent.workflow import AgentWorkflow
    from llama_index.core.workflow import Context
    from llama_index.core.workflow import JsonPickleSerializer, JsonSerializer


    def multiply(a: float, b: float) -> float:
        """Multiply two numbers and return the product"""
        return a * b

    def add(a: float, b: float) -> float:
        """Add two numbers and return the sum"""
        return a + b

    llm = Groq(model="llama3-70b-8192", api_key=groq_api_key)

    async def set_name(ctx: Context, name: str) -> str:
        state = await ctx.get("state")
        state["name"] = name
        await ctx.set("state", state)
        return f"Name set to {name}"


    workflow = AgentWorkflow.from_tools_or_functions(
        [set_name],
        llm=llm,
        system_prompt="You are a helpful assistant that can set a name.",
        initial_state={"name": "unset"},
    )

    ctx = Context(workflow)
    ctx_dict = ctx.to_dict(serializer=JsonSerializer())

    restored_ctx = Context.from_dict(
        workflow, ctx_dict, serializer=JsonSerializer()
            )
   


    async def main():
        
        response4 = await workflow.run(user_msg="What's my name?", ctx=ctx)
        print(str(response4))

    
        

    if __name__ == "__main__":
        import asyncio
        try:
            asyncio.run(main())
        except RuntimeError:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
else:
    print("GROQ_API key not found.")

    
