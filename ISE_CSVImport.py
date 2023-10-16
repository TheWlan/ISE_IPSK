import requests
import json
import csv
from creds import USERNAME, PASSWORD, ISE_IP  # Import credentials from creds.py

# Define the ISE API endpoint URL and credentials
ISE_BASE_URL = f"https://{ISE_IP}"

# Disable SSL certificate verification globally
session = requests.Session()
session.verify = False

# Function to authenticate with ISE and get group information
def get_group_information(group_name):
    # Authenticate with ISE
    auth = (USERNAME, PASSWORD)

    # Make a request to get group information with SSL verification disabled
    group_info_url = f"{ISE_BASE_URL}/ers/config/endpointgroup/name/{group_name}"
    response = session.get(
        group_info_url,
        auth=auth,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    )

    if response.status_code == 200:
        endpoint_group = json.loads(response.text).get("EndPointGroup")
        group_id = endpoint_group.get("id")
        return group_id
    else:
        print(f"Failed to get group information for '{group_name}' with status code:", response.status_code)
        return None

# Function to create or update an endpoint
def create_or_update_endpoint(name, description, mac, group_name):
    # Get the group ID from ISE
    group_id = get_group_information(group_name)

    if group_id is not None:
        # Check if the endpoint with the given MAC address already exists
        existing_endpoint = get_endpoint_details(mac)

        ISE_URL = f"{ISE_BASE_URL}/ers/config/endpoint"

        # If the endpoint exists, update it
        if existing_endpoint:
            endpoint_id = existing_endpoint["id"]
            payload = {
                "ERSEndPoint": {
                    "id": endpoint_id,
                    "name": name,
                    "description": description,
                    "mac": mac,
                    "groupId": group_id,
                    "staticGroupAssignment": True
                }
            }

            response = session.put(
                f"{ISE_URL}/{endpoint_id}",
                auth=(USERNAME, PASSWORD),
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )

            if response.status_code == 200:
                print(f"Endpoint with MAC address '{mac}' updated to group '{group_name}'")
            else:
                print(f"Failed to update endpoint with MAC address '{mac}' with status code:", response.status_code)
        else:
            # If the endpoint does not exist, create it
            payload = {
                "ERSEndPoint": {
                    "name": name,
                    "description": description,
                    "mac": mac,
                    "groupId": group_id,
                    "staticGroupAssignment": True
                }
            }

            response = session.post(
                ISE_URL,
                auth=(USERNAME, PASSWORD),
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )

            if response.status_code == 201:
                print(f"Endpoint '{name}' created in group '{group_name}'")
            else:
                print(f"Failed to create endpoint '{name}' with status code:", response.status_code)

# Function to get endpoint details by MAC address
def get_endpoint_details(mac):
    auth = (USERNAME, PASSWORD)

    # Make a request to get endpoint details with SSL verification disabled
    endpoint_details_url = f"{ISE_BASE_URL}/ers/config/endpoint?filter=mac.EQ.{mac}"
    response = session.get(
        endpoint_details_url,
        auth=auth,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    )

    if response.status_code == 200:
        endpoint_data = json.loads(response.text)
        resources = endpoint_data.get("SearchResult").get("resources")
        if resources:
            return resources[0]
    return None

# Read data from the CSV file
csv_file = "IPSK.csv"
with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        name = row["name"]
        description = row["description"]
        mac = row["mac"]
        group_name = row["group_name"]

        # Create or update the endpoint
        create_or_update_endpoint(name, description, mac, group_name)
