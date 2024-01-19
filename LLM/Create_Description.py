import os
import openai
from .Description_Template import Description_Template


api_key = os.getenv("OPENAI_API_KEY")

def Create_Description(Threat_Info=None, Bert_Report=None, Cortex_Report=None, Human_Report=None):
    gpt_prompt = Description_Template(Threat_Info, Bert_Report, Cortex_Report, Human_Report)
    message = [{"role": "user", "content": gpt_prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=message,
        temperature=0,
        max_tokens=2000,
        frequency_penalty=0.0
    )
    ans = response['choices'][0]['message']['content']
    print("GPT출력값: ", ans,"\n")
    
    return ans 