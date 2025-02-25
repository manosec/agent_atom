from llm import llm, system_prompt



class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role":"system", "content":system})
    
    def __call__(self, message):
        self.messages.append({"role":"user", "content":message})
        response = self.execute()
        self.messages.append(response)
        return response

    def execute(self):
        completion = llm.invoke(self.messages)
        return completion.content