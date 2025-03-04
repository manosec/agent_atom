from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from llm import groq_llm, gemini_llm
import os
from tools import store_tool

load_dotenv()

GROQ_KEY = os.getenv('GROQ_API_KEY')
GEMINI_KEY = os.getenv("GEMINI_API_KEY") 
print(GROQ_KEY)

artifact_manager = Agent(
    role="Artifact Manager",
    goal="""
        Your objective is to manage code artifacts by extracting the code content from the provided context and then using the available tools. When a code snippet is provided, you must:
        1. Extract the code content from the context.
        2. Analyze the content to determine the programming language (e.g. Python, Bash, JavaScript, etc.).
        3. Determine the appropriate file extension based on the language (e.g. .py for Python, .sh for Bash, .js for JavaScript).
        4. Save the snippet into a file by calling the tool with the three required parameters: code_snippet, file_name, and language.
        If the language is ambiguous or not explicitly clear, ask for clarification before proceeding.
        """,
    backstory="You are an automated Artifact Manager designed to help developers organize their code. With a deep understanding of various programming languages and file conventions, your role is to ensure that every code snippet is stored in a file that accurately reflects its language. This ensures that the files are ready for execution, debugging, or further development.",
    llm=gemini_llm,
    # tools=[store_tool],
    allow_delegation=False,
    api_key=GROQ_KEY
)


test_engineer = Agent(
    role="Test Engineer",
    goal="""
        Write clean, scalable, and maintainable code that complies with SOLID principles and best practices.
        
        Instructions:

        Break down tasks into modular, single-responsibility components.
        Prioritize code readability, reusability, and performance.
        Follow SOLID principles during design and implementation.
        Document key functions and design decisions.
        Write unit tests to validate functionality and edge cases.
        Proactively seek feedback and iterate on improvements.
        """,
    backstory="You are a passionate coder with a strong desire to improve. You thrive on feedback, continuously learning and refining your craft to deliver high-quality software.",
    llm=gemini_llm,
    allow_delegation=False,
    api_key=GROQ_KEY,
)

manager_llm = Agent(
    role="Senior Test Engineer / Testing Tech Lead",
    goal="""Review and provide constructive feedback on the code produced by the Software Engineer, ensuring it adheres to SOLID principles, scalability, and best practices.
           
            Instructions:

            Analyze the test code by test engineer for correctness, readability, and maintainability.
            Validate compliance with SOLID principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion).
            Suggest optimizations for performance and scalability.
            Identify potential edge cases and recommend test scenarios.
            Ensure code follows consistent naming conventions and documentation standards.
            Provide clear, actionable feedback with explanations.""",
    backstory="With years of experience in designing scalable systems, you are a meticulous and detail-oriented reviewer, guiding junior engineers toward writing production-grade software.",
    llm=gemini_llm,
    api_key=GROQ_KEY
)

artifact_manager_task = Task(
    description="""
                The task instructs the Artifact Manager to:
                1. Analyze a provided code snippet.
                2. Determine the programming language (e.g., Python, Bash, JavaScript, etc.).
                3. Assign the appropriate file extension based on the language (e.g., .py for Python, .sh for Bash).
                4. Save the code snippet into a file with a name that reflects its language.
                If the language cannot be confidently determined, the agent should ask for clarification before proceeding.
                """,
    expected_output="""
                The expected output is a confirmation message that includes:
                - The file name with the correct extension (e.g., 'artifact.py' for Python, 'artifact.sh' for Bash).
                - A confirmation that the file has been successfully saved.
                For example, upon processing a Python code snippet, the output might be: 
                "File artifact.py created successfully."
                """,
    agent=artifact_manager,
)

test_engineer_task = Task(
    description="""
                Generate an executable template script based on the provided test case scenario {message}. The script should be ready to accept parameters and run in the target environment.
                
                Instructions:

                Understand the scenario described in {message} and the target environment.
                Choose the appropriate scripting language (Python, Ansible, or others) based on the context.
                Design the script to accept external parameters (e.g., input variables or arguments).
                Include clear sections: Initialization, Execution, Parameter Handling, and Cleanup.
                Implement error handling, logging, and validation mechanisms.
                Ensure the script is idempotent and follows industry best practices.
                Add comments to explain key logic and parameter usage.
                """,
    expected_output="A fully executable, parameterized template script in the appropriate language, ready to be deployed on the target environment.",
    agent=test_engineer
)

manager_task = Task(
    description="""Review the template script generated by the Test Engineer based on the provided test case scenario {message}. Ensure the script meets functional, performance, and maintainability standards before execution in the target environment.
                    
                    Instructions:
                    
                    Validate that the script language aligns with the environment requirements.
                    Assess whether the script correctly handles input parameters and external dependencies.
                    Ensure the script follows best practices (idempotency, modularity, and error handling).
                    Identify potential failure points and recommend error-handling improvements.
                    Check for scalability, security considerations, and performance optimizations.
                    Review comments and documentation for clarity and completeness.
                    Provide actionable feedback on the overall structure and adherence to coding standards.""",

    expected_output="A refined template script with constructive feedback and necessary modifications, ensuring the script is ready for deployment.",
    agent=manager_llm
)



crew = Crew(
    agents=[test_engineer, manager_llm],
    tasks=[test_engineer_task, manager_task],
    process=Process.sequential,
    memory=True,
    embedder={
        "provider": "google",
        "config": {
            "api_key": GEMINI_KEY,
            "model": "models/embedding-001"
        }
    },
    verbose=True,
)

if query := input("Enter the chaos test case:"):
    result  = crew.kickoff(inputs={"message":query})
    print(result)
