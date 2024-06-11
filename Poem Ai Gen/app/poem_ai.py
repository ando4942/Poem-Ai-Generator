import openai
from dotenv import load_dotenv
import os
import argparse

MAX_CHAR_LEN = 32

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parser_args()
    user_input = args.input()
    if validate_len(user_input):
        gen_poem(user_input)
    else:
        raise ValueError(f"Inupt lenght is too long. Must be under {MAX_CHAR_LEN} characters.")

def validate_len(user_input):
    return len(user_input) < MAX_CHAR_LEN



def gen_poem(user_input):
    load_dotenv()
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    prompt = f"Write a haiku poem about {user_input}."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    print(response.choices[0].message['content'])
    return response.choices[0].message['content']

if __name__ == "__main__":
    main()
