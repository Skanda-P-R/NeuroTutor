from groq import Groq
import os

client = Groq(
    api_key=os.getenv("groq_api"),
)

def get_code(diff):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": '''Generate a Python code snippet that includes intentional errors, based on a specified difficulty level.

If the difficulty is easy, include basic syntax or logical mistakes (e.g., missing colons, incorrect indentation, undefined variables).

If the difficulty is medium, include more subtle errors (e.g., off-by-one indexing, misuse of built-in functions, incorrect use of loops or conditionals).

If the difficulty is hard, include complex logic flaws, misused algorithms, incorrect recursion, or subtle issues that require deeper debugging knowledge.

Return only the code in a single Python code block, and ensure that the errors align with the selected difficulty level.'''
            },
            {
                "role": "user",
                "content": "Difficulty Level: " + diff + "\n",
            }
        ],
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
    )

    return chat_completion.choices[0].message.content

def compare(e_code,u_code):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": '''You are a Python code reviewer.

You will be given two code snippets:

- Code 1: This code contains one or more errors.
- Code 2: This is an attempt to fix the errors from Code 1.

Your task is to:

1. Carefully compare Code 1 and Code 2.
2. Determine whether **Code 2** has successfully fixed **all** the issues that were present in Code 1.
3. If Code 2 has fixed all errors, reply with only:
Good job debugging all errors!
4. If any issues still exist in Code 2, reply with:
Sorry, but you didn't correct all errors. Here are the remaining issues:

Then provide a clear, accurate, and concise list of what is still wrong in Code 2. **Do not invent errors. Only point out real issues.**
''',
            },
            {
                "role": "user",
                "content": "Code 1: " + e_code + "\n\nCode 2: " + u_code + "\n",
            }
        ],
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
    )

    return chat_completion.choices[0].message.content