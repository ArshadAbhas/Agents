import pandas as pd
from openai import OpenAI
from context import Context

# --- Step 1: Setup NVIDIA API Client ---
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=""
)

# --- Step 2: Model Call Function ---
def get_model_response(prompt: str) -> str:
    response_text = ""

    completion = client.chat.completions.create(
        model="nvidia/llama-3.3-nemotron-super-49b-v1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        top_p=0.95,
        max_tokens=4096,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content:
            response_text += chunk.choices[0].delta.content

    return response_text

# --- Step 3: Create Prompt from DataFrame ---
def dataframe_to_prompt_from_context(context: Context) -> str:
    columns = context.extract_column_names()
    sample = context.sample()

    prompt = f"""
You are a smart data analyst.

Here is a dataset with the following columns:
{columns}

Here are the first {context.rows} rows of the data:

{sample}

Based on the above i want three things from you
1. Provide me whats about the data .
2. Provide me general insights about the data 
3. Get me some questions which i can ask the csv_agent  to get the numerical support  so that the insights can be supported
4. Suggest me which graphs i can use and with which data present in the data frame 
5. Generate the code to generate the graph


"""
    return prompt


# --- Step 4: Main Entry Point ---
def generate_csv_insights(file_path: str):
    df = pd.read_csv(file_path)
    prompt = dataframe_to_prompt_from_context(df)
    insights = get_model_response(prompt)
    return insights

# --- Step 5: Run ---
if __name__ == "__main__":
    file_path = "/home/arshad-ahmed/Documents/Agents/Sample_Data/Bakery.csv"
    df = pd.read_csv(file_path)

    # Create context
    context = Context(df, rows=500)

    # Generate prompt using the context
    prompt = dataframe_to_prompt_from_context(context)

    # Pass to model (e.g., OpenAI, Mistral, Nematron etc.)
    insights = get_model_response(prompt)

    print("\n📊 Insights:\n")
    print(insights)

