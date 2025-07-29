from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=

def get_model_response(prompt: str) -> str:
    response_text = ""

    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content:
            response_text += chunk.choices[0].delta.content

    return response_text
