import requests
import json

# Define the ISE server details
ise_ip = "10.40.0.210"
username = "admin"
password = "P@ssword1"

# Define the API endpoint URL
url = f"https://{ise_ip}:9060/ers/config/endpointgroup"

# Define the headers and authentication details
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
auth = (username, password)

# Send the API request and get the response
response = requests.get(url, headers=headers, auth=auth, verify=False)

# Print the list of endpoint groups
if response.status_code == 200:
    groups = json.loads(response.text)['SearchResult']['resources']
    for group in groups:
        print(group['name'])
else:
    print("Failed to get endpoint groups. Status code:", response.status_code)
