from agent_builder import Agent
from llm import system_prompt
import re
import requests


conversation_agent = Agent(system_prompt)


print(conversation_agent("hi"))
print(conversation_agent.messages)


def add_operation(ops):
    r = request.get("url")

def multiplication(ops):
    return eval(ops)

known_action = {
    "add_operation":add_operation,
    "multiplication":multiplication
}


actions_re = re.compile(' ^Action: (\w+): (.*)$')

def query(question, max_turns):
    turn = 0
    bot = Agent(system_prompt)
    query = question

    while turn < max_turns:
        print("inside while")
        turn += 1
        response = bot(query)
        actions = [actions_re.match(a) for a in response.split("\n") if actions_re.match(a)]
        print(response)
        if actions:
            action, action_input = actions[0].groups()
            print("---Running---{} with {}".format(action, action_input))
            if action not in known_action:
                raise Exception(f"Unkown action {action}")
            function_output = known_action[action](action_input)
            print(query)
            query = f"Observation: {function_output}"
        else:
            return 

query("What is the addition of 7 and 8. and the result should be product with 10. give me the final answer", 5)

        

