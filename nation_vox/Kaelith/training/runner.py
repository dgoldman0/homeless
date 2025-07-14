# Executes a chain of operations starting from a prompt to a final output, with intermediate steps.
import openai
import json
import time 

client = openai.Client()

core_model = "gpt-4.1"
#custom_model = "gpt-4.1-vox-2024-10-10"
custom_model = "gpt-4.1"


# Function that generates a signature for user input by giving a list of 25 keywords that uniquely identify it. The LLM will be instructed to generate a list of 25 keywords that best summarize the input, in order.
def generate_process_signature(thought_process):
    max_keywords = 25
    keywords = []

    # Cap of 100 just prevents endless loops but should never be reached because it's unlikely the LLM won't produce new keywords
    attempts = 0
    while len(keywords) < max_keywords and attempts < 100:
        response = client.chat.completions.create(
            model=core_model,
            messages=[
                {"role": "system", "content": f"Generate a comma-separated list of {max_keywords} keywords that best summarize and uniquely identify the following thought process. Focus on the more recent developments. Only output the keywords, separated by commas."},
                {"role": "user", "content": json.dumps(thought_process)},
            ],
            max_tokens=150,
            temperature=0.7,
            n=1,
        )
        output = response.choices[0].message.content.strip()
        # Parse output into keywords
        new_keywords = [kw.strip() for kw in output.split(",") if kw.strip()]
        # Add new keywords to the list, avoiding duplicates
        for kw in new_keywords:
            if kw not in keywords:
                keywords.append(kw)
            if len(keywords) >= max_keywords:
                break
        attempts += 1

    return sorted(list(keywords))[:max_keywords]
 
def process_user_input(input):
    system_prompt = "You are the Kaelithi National Vox in Signature Mode. You will be given a signature. If you are also given a question, you will answer it in a single, clear sentence. If you are given only a signature, you will give a bunch of one sentence thoughts relating to the signature, one per line."

    thought_process = []

    current_input = input
    passes = 1
    while True:
        print(f"Pass #{passes}")
        passes += 1
        # Get signature
        signature = generate_process_signature(current_input)
        thought_process.append({"input": current_input, "timestamp": time.time(), "signature": signature})

        # Use the custom model with the format from main.py to get a signature only generation...
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"<SIG>: {signature}"}
        ]

        response = client.chat.completions.create(
            model=custom_model,
            messages=messages,
            max_tokens=300,
            temperature=0.7,
            n=1,
        )
        output = response.choices[0].message.content.strip()
        
        # Append to thought process
        thought_process.append({"thought": output, "timestamp": time.time()})

        # Use as input to main model to identify how, if at all, it relates to the user input, and to end with <FINAL>\nResponse IF there is now enough information to respond. Otherwise do not include <FINAL>.
        followup_server_prompt = (
            f"You are the Kaelithi National Vox. You are either starting are continuing a conversation. Determine how, if at all, the following thoughts relate to the current state of the thought process. If there is enough information to respond to the user input, end your response with <FINAL> followed by a newline and your response. If there is not enough information to respond, do not include <FINAL>.\n\n"
        )

        followup_response = client.chat.completions.create(
            model=core_model,
            messages=[
                {"role": "system", "content": followup_server_prompt},
                {"role": "user", "content": f"Thoughts:\n{output}\n\nThought process:\n{thought_process}"}
            ],
            max_tokens=300,
            temperature=0.7,
            n=1,
        )
        followup_output = followup_response.choices[0].message.content.strip()

        # Check if <FINAL> is in the output
        if "<FINAL>" in followup_output:
            final_index = followup_output.index("<FINAL>")
            final_response = followup_output[final_index + len("<FINAL>"):].strip()
            # Append the final response to the thought process less the <FINAL> tag or anything after it
            thought_process.append({"final_thought": followup_output[:final_index].strip(), "timestamp": time.time()})
            return final_response, thought_process
        else:
            current_input = followup_output

if __name__ == "__main__":
    user_input = input("Enter your input: ")
    final_response, thought_process = process_user_input(user_input)
    print("Final Response:", final_response)
    print("Thought Process:")
    for step in thought_process:
        print(json.dumps(step, indent=2))
