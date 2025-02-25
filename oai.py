from openai import OpenAI
import os

os.environ['OPENAI_API_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcHAiLCJleHAiOjE3OTk5OTk5OTksInN1YiI6Mjc3MDI3OCwiYXVkIjoiV0VCIiwiaWF0IjoxNjk0MDc2ODUxfQ.0CUH2btAFSJXXLsQ-Q49z2Vnh_-WZc7mVG3lIiPbE30'
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

client = OpenAI()


chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
)