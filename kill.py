from gradio_client import Client, handle_file

client = Client("https://fc7b45c64739cf615a.gradio.live/")
result = client.predict(
	file=handle_file(r'/home/arshad-ahmed/Documents/Agents/Sample_Data/sap final dataset.xlsx'),
	api_name="/predict"
)
print(result)