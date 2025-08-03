# from openai import OpenAI

# client = OpenAI(
#     base_url="https://integrate.api.nvidia.com/v1",
#     api_key="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"
# )

# def get_model_response(prompt: str) -> str:
#     response_text = ""

#     completion = client.chat.completions.create(
#         model="nvidia/llama-3.1-nemotron-70b-instruct",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.5,
#         top_p=1,
#         max_tokens=1024,
#         stream=True
#     )

#     for chunk in completion:
#         if chunk.choices[0].delta.content:
#             response_text += chunk.choices[0].delta.content

#     return response_text
# def input_User(report,userquery) -> str:
#     prompt = '''
#     you are an intelligent analyst who is capable of generating a report based on the input data provided by the user.
#     You are  provided with a summary of the data. Along with the report attach the answers for the  user query at the end.
#     '''+ f''' the report would be {report}''' + f'''+ the user query is {userquery}'''
#     return prompt

