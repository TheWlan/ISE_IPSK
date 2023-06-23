import requests
import json

# Define the ISE API endpoint URL and credentials
ISE_IP = "10.40.0.210"
GROUP_NAME = "VLAN30"
ISE_URL = f"https://{ISE_IP}/ers/config/endpointgroup/name/{GROUP_NAME}"
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



ISE_URL = "https://10.40.0.210/ers/config/endpoint"
payload = {
    "ERSEndPoint": {
        "name": "MyEndpoint1",
        "description": "MyEndpoint1",
        "mac": "11:22:33:44:55:73",
        "groupId": group_id,
        "staticGroupAssignment": True
    }
}

# Send the API request to create the endpoint
response = requests.post(
    ISE_URL,
    auth=(USERNAME, PASSWORD),
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload),
    verify=False
)

# Check the response status code
if response.status_code == 201:
    print("Endpoint created successfully")
else:
    print("Endpoint creation failed with status code:", response.status_code)

