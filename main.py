from model import get_model_response

# Read prompt from file
with open("input.txt", "r") as file:
    prompt = file.read().strip()

# Debug: print prompt length
print(f"Prompt length: {len(prompt)}")
print(f"Prompt preview: {prompt[:50]}")

if not prompt:
    print("❗ Error: input.txt is empty or has only spaces.")
else:
    response = get_model_response(prompt)

    print("\n--- Response Start ---\n")
    print(response)
    print("\n--- Response End ---\n")

    with open("output.txt", "w") as f:
        f.write(response)
