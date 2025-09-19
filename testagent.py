from langchain_nvidia_ai_endpoints import ChatNVIDIA

# client = ChatNVIDIA(
#   model="qwen/qwen3-coder-480b-a35b-instruct",
#   api_key="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", 
#   temperature=0.7,
#   top_p=0.8,
#   max_tokens=4096,
# )
llm = ChatNVIDIA(
    model="qwen/qwen3-coder-480b-a35b-instruct",
    api_key=""   # replace with your NVIDIA API key
)

print(llm.invoke("hi"))
  
