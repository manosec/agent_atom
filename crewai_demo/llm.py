from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

from crewai import LLM

load_dotenv()

llm = LLM(
    model="groq/deepseek-r1-distill-qwen-32b",
    temperature=0.0
)

model = "deepseek-r1-distill-qwen-32b"

api_key = os.getenv("groq_api_key")

# llm = ChatGroq(model=model, api_key=api_key, temperature=0.0)

system_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

add_operation:
e.g. add_operation: 10 + 7 = 17
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

multiplication:
e.g. multiplication: 6 * 6 = 36
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

Example session:

Question: What is the addition of 7 + 10?
Thought: I should perform addition operation using add_operation
Action: add_operation: 7, 10
PAUSE

You will be called again with this:

Observation: The result of the operation is 17.

You then output:

Answer: The addition operation is 17.
""".strip()
