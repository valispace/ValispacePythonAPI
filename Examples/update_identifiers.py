import valispace

"""
This script gets all Specification Abbreviations and rename all requirements (identifiers) with the abbreviation as prefix
plus a numerical indication with a defined number of digits.
The requirements identifier will be ordered by the creation date, but this can be modified in the "sorted" function.
If no abbreviation is defined in a specification, requirements will take REQ as a prefix.
"""

project_id = PROJECT_ID
valispace_url = "https://<your_company>.valispace.com/"

valispace = valispace.API(valispace_url)

# Get all requirements for the project and create a dictionary mapping requirement IDs to requirements
requirements = valispace.request("GET", "requirements/?project="+str(project_id))
req_mapping = {req["id"]: req for req in requirements}

# Get all specifications for the project
specifications = valispace.request("GET", "requirements/specifications/?project="+str(project_id))

# Define the number of digits for the identifier and the starting number
num_identifier_digits = 4
start_number = 1

# Loop through each specification
for spec in specifications:
    # Get the abbreviation for the specification. If no abbreviation, uses "REQ" as default
    abbreviation = spec.get("abbr", "REQ")

    # Get all requirements for the specification and sort them by creation date
    spec_reqs = [req_mapping[req_id] for req_id in spec["requirements"]]
    sorted_requirements_by_creation = sorted(spec_reqs, key=lambda x: x['created'])

    # Loop through each requirement and update its identifier
    for i, req in enumerate(sorted_requirements_by_creation, start_number):
        identifier_number = str(i).zfill(num_identifier_digits)
        new_identifier = f"{abbreviation}-{identifier_number}"

        print(new_identifier)

        # Update the identifier for the requirement in Valispace
        valispace.request("PATCH", f"requirements/{req['id']}/", {"identifier": new_identifier})
