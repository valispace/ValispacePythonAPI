from valispace import API
import requests

# Constants for the project ID and Valispace credentials
PROJECT_ID = <PROJECT_ID>  # Replace with your project ID
VALISPACE = {
    'domain': 'https://<YOUR_DEPLOYMENT>.valispace.com/',  # Valispace domain URL
    'username': '',  # Valispace account username
    'password': ''   # Valispace account password
}


def main():
    # Initializing the Valispace API with credentials and domain
    api = API(
        url = VALISPACE.get('domain'),
        username = VALISPACE.get('username'),
        password = VALISPACE.get('password'),
        warn_https = VALISPACE.get('warn_https', False),  # Disable HTTPS warnings if necessary
    )

    # Fetching requirements and specifications from the Valispace API
    requirements = api.get(f"requirements/?project={PROJECT_ID}")
    specifications = api.get(f"requirements/specifications/?project={PROJECT_ID}")

    # Updating position of specifications based on a key identifier
    update_position_by_key_within_spec(api, specifications, requirements, key="identifier")

# Function to update position of specifications based on a given key
def update_position_by_key_within_spec(api, specifications, requirements, key="created"):
    bulk_update_payload = {}  # Dictionary to store update information
    spec_counter = 1  # Counter for specifications
    for specification in specifications:
        req_counter = 0.1  # Sub-counter for requirements within a specification
        # Filtering requirements that belong to the current specification
        spec_requirements = [req for req in requirements if req["id"] in specification["requirements"]]
        # Sorting requirements based on the specified key
        sorted_requirements = sorted(spec_requirements, key=lambda x: x[key])
        for req in sorted_requirements:
            # Preparing the update payload
            bulk_update_payload[req["id"]] = {"position": spec_counter+req_counter}
            req_counter += 0.1  # Incrementing sub-counter
        spec_counter += 1  # Incrementing main counter

    try:
        # Sending a POST request to update requirements in bulk
        response = api.request("POST", "requirements/bulk-update/", bulk_update_payload)    
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")  # Printing HTTP error if any


# Function to update position of requirements based on a given key
def update_position_by_key(api, requirements, key="created"):
    bulk_update_payload = {}  # Dictionary to store update information
    # Sorting requirements based on the specified key
    sorted_requirements = sorted(requirements, key=lambda x: x[key])
    counter = 1  # Counter for requirements
    for requirement in sorted_requirements:
        # Preparing the update payload
        bulk_update_payload[requirement['id']] = {"position": counter}
        counter += 1  # Incrementing the counter

    try:
        # Sending a POST request to update requirements in bulk
        response = api.request("POST", "requirements/bulk-update/", bulk_update_payload)    
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")  # Printing HTTP error if any


main()