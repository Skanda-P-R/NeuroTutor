from groq import Groq
import os

client = Groq(
    api_key=os.getenv("groq_api"),
)

def send_to_groq(code,error):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a code debugger system, which gives only the corrected code based on the user code and the error list supplied."
            },
            {
                "role": "user",
                "content": "Code: " + code + "\nError List: " + error,
            }
        ],
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
    )

    return chat_completion.choices[0].message.content