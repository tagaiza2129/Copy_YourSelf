import requests
import json

# Define the URL of the endpoint
url = 'http://localhost:2192/learning'

#model_name=data["model_path"]
#lr=data["lr"]
#epoch=data["epoch"]
#batch_size=data["batch_size"]
#device_type=data["device_type"]
#device_id=data["device_id"]
# Define the JSON data to send
data = {
    'epoch': '100',
    'batch_size': '32',
    'device_type': 'METAL',
    'device_id': '0',
    'lr': '0.001',
    'model_path': 'Learning_test_model',
}

# Convert the data to JSON format
json_data = json.dumps(data)

# Set the headers for the request
headers = {
    'Content-Type': 'application/json'
}

# Send the POST request
response = requests.post(url, data=json_data, headers=headers)

# Check the response status code
if response.status_code == 200:
    print('POST request successful')
else:
    print('POST request failed')