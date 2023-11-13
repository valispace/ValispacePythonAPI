from valispace import API
import requests

PROJECT_ID = <PROJECT_ID>
VALISPACE = {
        'domain': 'https://<YOUR_DEPLOYMENT>.valispace.com/',
        'username': '',
        'password': ''
    }

def main():
    
    
    api = API(
        url = VALISPACE.get('domain'),
        username = VALISPACE.get('username'),
        password = VALISPACE.get('password'),
        warn_https = VALISPACE.get('warn_https', False),
    )

    requirements = api.get(f"requirements/?project={PROJECT_ID}")
    specifications = api.get(f"requirements/specifications/?project={PROJECT_ID}")

    # update_position_by_key(api, requirements, key="created")
    update_position_by_key_within_spec(api, specifications, requirements, key="identifier")

def update_position_by_key_within_spec(api, specifications, requirements, key="created"):
    bulk_update_payload = {}
    spec_counter = 1
    for specification in specifications:
        req_counter = 0.1
        spec_requirements = [req for req in requirements if req["id"] in specification["requirements"]]
        sorted_requirements = sorted(spec_requirements, key=lambda x: x[key])
        for req in sorted_requirements:
            bulk_update_payload[req["id"]] = {"position": spec_counter+req_counter}
            req_counter += 0.1
        spec_counter += 1

    try:
        response = api.request("POST", "requirements/bulk-update/", bulk_update_payload)    
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")    



def update_position_by_key(api, requirements, key="created"):
    bulk_update_payload = {}
    sorted_requirements = sorted(requirements, key=lambda x: x[key])
    counter = 1
    for requirement in sorted_requirements:
        bulk_update_payload[requirement['id']] = {"position": counter}
        counter += 1

    try:
        response = api.request("POST", "requirements/bulk-update/", bulk_update_payload)    
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")

main()