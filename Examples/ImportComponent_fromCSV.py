import csv
import valispace

# in this example "component.csv" should be a table with Name and Parent as headers.
# where Parent is the full path of the component. In the same format you get when
# you export the Components table from Valispace

valispace = valispace.API(url="https://<your_url>.valispace.com/", username=None, password=None)

project_id =
file_name = 'components.csv'


# Initialize a dictionary to store component IDs
component_ids = {}

# Read the CSV file
with open(file_name, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row

    for row in csvreader:
        component_name, parent_path = row

        # Determine the parent ID
        parent_id = None
        if parent_path:
            parent_names = parent_path.split('.')
            parent_name = parent_names[-1]  # The last name in the path is the immediate parent
            parent_id = component_ids.get(parent_name)  # Get the parent ID from the dictionary

            if parent_id is None:
                print(f"Error: Parent {parent_name} not found for {component_name}")
                continue  # Skip this row and continue with the next one

        # Create the component
        component_data = {
            "name": component_name,
            "project": project_id,
            "parent": parent_id
        }

        component_posted = valispace.post("components/", component_data)

        # Save the component ID in the dictionary
        component_id = component_posted["id"]
        component_ids[component_name] = component_id
