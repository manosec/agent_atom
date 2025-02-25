from crewai import Agent, Task, Crew
from llm import llm


friendly_agent = Agent(
    role="Friend",
    goal="Providing response in more friendly and empathetic manner",
    backstory="Assitant who have gone through several hardships and possess lot of wisdom on how to lead a life in more better and lovely way and who have the beautiful & positive outlook on life",
    llm=llm,
    allow_delegation=False
)

task = Task(
    description="{message}",
    expected_output="friendly and thoughtful response",
    agent=friendly_agent
)

crew = Crew(
    agents=[friendly_agent],
    tasks=[task],
    verbose=2
)

result = crew.kickoff(inputs={"message":"hi there"})

print(result)