import openai

client = openai.Client(base_url="http://127.0.0.1:30000/v1", api_key="EMPTY")

def chat(prompt, temperature=0):
    response = client.chat.completions.create(
        model="default",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant"},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=1024,
    )
    return response.choices[0].message.content

def complete(prompt, temperature=0):
    response = client.completions.create(
        model="default",
        prompt=prompt,
        temperature=temperature,
        max_tokens=1024,
    )
    return response.choices[0].text