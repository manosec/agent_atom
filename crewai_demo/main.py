from crewai import Agent, Task, Crew
from llm import llm


friendly_agent = Agent(
    role="Friend",
    goal="Providing response in more friendly and empathetic manner",
    backstory="Assistant who have gone through several hardships and possess lot of wisdom on how to lead a life in more better and lovely way and who have the beautiful & positive outlook on life",
    llm=llm,
    allow_delegation=False,
    api_key="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"
)

task = Task(
    description="{message}",
    expected_output="friendly and thoughtful response",
    agent=friendly_agent
)

crew = Crew(
    agents=[friendly_agent],
    tasks=[task],
    verbose=True
)

messages = []

while True:

    if input_string := input("Enter your query >"):
        result = crew.kickoff(inputs={"message":messages})
        messages.append(result)

    print(result)