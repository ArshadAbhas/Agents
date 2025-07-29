from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

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
