import requests
import json

# Define the ISE API endpoint URL and credentials
ISE_URL = "https://10.40.0.210/ers/config/endpointgroup/name/iPSK_VLAN10"
USERNAME = "admin"
PASSWORD = "P@ssword1"

# Send the API request to get the endpoint group details
response = requests.get(
    ISE_URL,
    auth=(USERNAME, PASSWORD),
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json"
    },
    verify=False
)

# Print the response text for troubleshooting
#print(response.text)

# Parse the response JSON to extract the groupId
if response.status_code == 200:
    endpoint_group = json.loads(response.text).get("EndPointGroup")
    group_id = endpoint_group.get("id")
    print(f"The groupId for VLAN10 is {group_id}")
else:
    print("Failed to retrieve endpoint group details with status code:", response.status_code)


