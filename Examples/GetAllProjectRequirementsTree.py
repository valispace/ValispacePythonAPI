"""
pip install valispace
https://github.com/valispace/ValispacePythonAPI
"""

import argparse
import os.path
import re
from collections import deque

from valispace import API


class ValispaceDataContainer:
    """
    This helper class stores the data necessary for a complete iteration over a
    project's requirements tree. Additionally, the class provides the iterator
    methods.

    # Valispace supports the following entities for structuring the requirements:
    # 1) Folders
    # 2) Specifications. A specification corresponds to a requirement document.
    #    A specification can be either contained in a folder or be at the project's
    #    top-level without being included to any folder.
    # 3) Groups. A group corresponds to a chapter in a Specification. A group
    #    can be only found within a specification.
    # 4) Requirements.
    #    A requirement can only be found within a specification. Within a specification,
    #    it can be contained within a group or be at the specification's top level.
    """

    def __init__(self, map_id_to_folders, map_id_to_specs, map_id_to_groups, map_id_to_reqs, top_level_folders):
        self.map_id_to_folders = map_id_to_folders
        self.map_id_to_specs = map_id_to_specs
        self.map_id_to_groups = map_id_to_groups
        self.map_id_to_reqs = map_id_to_reqs
        self.top_level_folders = ValispaceDataContainer.sort_folders_by_name_key(top_level_folders)

    @staticmethod
    def sort_folders_by_name_key(folders):
        def convert(text): int(text) if text.isdigit() else text.lower()
        return sorted(
            folders,
            key=lambda name_: [convert(c) for c in re.split('([0-9]+)', name_["name"])]
        )

    def iterate_folders(self):
        task_list = deque(map(lambda tlf: (tlf, []), self.top_level_folders))

        while len(task_list) > 0:
            current_folder, current_parent_stack = task_list.popleft()

            yield current_folder, current_parent_stack

            children_ids = current_folder["children"]
            new_parent_stack = current_parent_stack + [current_folder]

            unsorted_children = list(map(lambda ch_id: self.map_id_to_folders[ch_id], children_ids))
            sorted_children = ValispaceDataContainer.sort_folders_by_name_key(unsorted_children)

            children_pairs = reversed(list(map(lambda child: (child, new_parent_stack), sorted_children)))

            task_list.extendleft(children_pairs)

    def iterate_folder_specs(self, folder):
        folder_specs_ids = folder["items"] if "items" in folder else []
        yield from map(
            lambda folder_id: self.map_id_to_specs[folder_id], folder_specs_ids
        )

    def iterate_top_level_specs(self):
        """
        Not all Specs are attached to Groups. Specs can be also present on the
        root-level and have their 'folder' equal None. This method enumerates
        over these freestanding specs.
        """
        return filter(
            lambda spec: spec["folder"] is None, self.map_id_to_specs.values()
        )

    def iterate_spec_groups(self, spec):
        spec_groups_ids = spec["requirement_groups"]
        spec_groups = map(
            lambda group_id: self.map_id_to_groups[group_id], spec_groups_ids
        )
        task_list = deque(map(lambda tlf: (tlf, []), spec_groups))

        # Valispace stores group children in a special way:
        # both direct children and non-direct children are stored in "children".
        # We maintain a set of visited items to prevent the algorithm from
        # visiting the same nodes several times.
        visited = set()
        while len(task_list) > 0:
            current_folder, current_parent_stack = task_list.popleft()
            if current_folder["id"] in visited:
                continue

            visited.add(current_folder["id"])

            yield current_folder, current_parent_stack

            spec_groups_ids = current_folder["children"]
            new_parent_stack = current_parent_stack + [current_folder]

            spec_groups = map(
                lambda group_id: self.map_id_to_groups[group_id], spec_groups_ids
            )

            children_pairs = reversed(list(map(lambda child: (child, new_parent_stack), spec_groups)))

            task_list.extendleft(children_pairs)

    def iterate_spec_requirements(self, spec):
        """
        Requirements can be attached to a requirements group, or they can be standalone,
        without a group. This method iterates over the standalone requirements.
        For iterating over the group-contained requirements, see another
        method iterate_group_requirements().
        """
        requirements_ids = spec["requirements"] if "requirements" in spec else []
        yield from map(
            lambda requirement_id: self.map_id_to_reqs[requirement_id], requirements_ids
        )

    def iterate_group_requirements(self, group):
        requirements_ids = group["requirements"] if "requirements" in group else []
        yield from map(
            lambda requirement_id: self.map_id_to_reqs[requirement_id], requirements_ids
        )


class ProjectTreeIterator:
    def __init__(self):
        """
        This example helper class demonstrates how the iteration methods of the
        ValispaceDataContainer class can be used to achieve a complete iteration
        over a Valispace project's requirements tree.

        Below in this __init__ function, the iterator can be extended with extra
        options for what should be iterated or skipped. The iterator function
        can use these options for a customized iteration.
        """
        pass

    def iterate(self, container: ValispaceDataContainer):
        folders_iterated = 0
        specs_iterated = 0
        groups_iterated = 0
        requirements_iterated = 0

        for folder, folder_parents in container.iterate_folders():
            folders_iterated += 1
            folder_names = list(map(lambda pf: pf["name"], folder_parents))
            folder_names.append(folder["name"])
            path_to_folder = os.path.join(*folder_names)
            print(f"Iterating folder: {path_to_folder}")

            for spec in container.iterate_folder_specs(folder):
                specs_iterated += 1

                spec_name = spec["name"]

                print(f"Iterating spec: {spec_name}")

                reqs_visited = set()
                for group, group_parents in container.iterate_spec_groups(spec):
                    groups_iterated += 1

                    group_name = group["name"]
                    print(f"Iterating group: {group_name}")

                    for requirement in container.iterate_group_requirements(group):
                        requirements_iterated += 1

                        requirement_id = requirement.get("id", "<No identifier>")
                        reqs_visited.add(requirement_id)

                        requirement_uid = requirement.get("identifier", "<No identifier>")
                        print(f"Iterating requirement: {requirement_uid}")

                for requirement in container.iterate_spec_requirements(spec):
                    if requirement["id"] in reqs_visited:
                        continue
                    requirements_iterated += 1

                    requirement_uid = requirement.get("identifier", "<No identifier>")
                    print(f"Iterating requirement: {requirement_uid}")

        for _ in container.iterate_top_level_specs():
            specs_iterated += 1

        print(f"Iteration results:")
        print(f"Folders: {folders_iterated}")
        print(f"Specs: {specs_iterated}")
        print(f"Groups: {groups_iterated}")
        print(f"Requirements: {requirements_iterated}")

        assert folders_iterated == len(container.map_id_to_folders.values())
        assert specs_iterated == len(container.map_id_to_specs.values())
        assert groups_iterated == len(container.map_id_to_groups.values())
        assert requirements_iterated == len(container.map_id_to_reqs.values())


def main():
    parser = argparse.ArgumentParser(description='Valispace requirements export script.')
    parser.add_argument("username", help='Valispace user name.')
    parser.add_argument("password", help='Valispace user password.')
    parser.add_argument("valispace_url", help='Valispace URL, e.g., https://mycompany.valispace.com.')
    parser.add_argument("project_id", help='Valispace project ID.')
    args = vars(parser.parse_args())

    username = args["username"]
    password = args["password"]
    valispace_url = args["valispace_url"]
    project_id = args["project_id"]

    valispace = API(url=valispace_url, username=username, password=password)

    top_level_folders = []
    map_id_to_folders = {}
    map_id_to_specs = {}
    map_id_to_groups = {}
    map_id_to_reqs = {}

    print("FOLDERS")
    result = valispace.get_folders(project_id)
    for entry_ in result:
        map_id_to_folders[entry_["id"]] = entry_
        if entry_["parent"] is None:
            top_level_folders.append(entry_)
    print(f"FOLDERS: {len(result)} total")

    print("SPECS")
    result = valispace.get_specifications(project_id)
    for entry_ in result:
        map_id_to_specs[entry_["id"]] = entry_
    print(f"SPECS: {len(result)} total")

    print("GROUPS")
    result = valispace.get_groups(project_id)
    for entry_ in result:
        map_id_to_groups[entry_["id"]] = entry_
    print(f"GROUPS: {len(result)} total")

    print("REQS:")
    result = valispace.get_requirements(project_id)
    for requiremnt in result:
        map_id_to_reqs[requiremnt["id"]] = requiremnt
    print(f"REQS: {len(result)} total")

    container = ValispaceDataContainer(
        map_id_to_folders=map_id_to_folders,
        map_id_to_specs=map_id_to_specs,
        map_id_to_groups=map_id_to_groups,
        map_id_to_reqs=map_id_to_reqs,
        top_level_folders=top_level_folders
    )

    project_tree_iterator = ProjectTreeIterator()
    project_tree_iterator.iterate(container)


main()
