from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

completion = client.chat.completions.create(
  model="nvidia/nvidia-nemotron-nano-9b-v2",
 messages=[
    {"role": "system", "content": "You are a good friend and archaeologist."},
    {"role": "user", "content": "Yo how about a world where we coexist with dinosaurs?"}
],
  temperature=0,
  top_p=0.95,
  max_tokens=2048,
  frequency_penalty=0,
  presence_penalty=0,
  stream=True,
  extra_body={
    "min_thinking_tokens": 1024,
    "max_thinking_tokens": 2048
  }
)

for chunk in completion:
  reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
  if reasoning:
    print(reasoning, end="")
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")


