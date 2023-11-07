"""
pip install valispace
https://github.com/valispace/ValispacePythonAPI
"""

import argparse
import pprint
import re
from dataclasses import dataclass, field
from typing import Set

from valispace import API


@dataclass
class ValispaceDataSpecIterationContext:
    """
    This data container class is used during the iteration over the downloaded
    Valispace requirements (i.e., folders, specs, groups, requirements).
    Valispace stores group data and requirements with redundancy. For example:
    A spec group typically contains links to its own requirements as well as the
    requirements of its child spec groups. Since this script provides the
    depth-first iteration, this context class collects the already visited
    requirements and spec groups, which are used by the iterator to not yield
    these objects more than once.
    """
    all_spec_requirements: Set = field(default_factory=set)
    all_spec_groups: Set = field(default_factory=set)


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

    def __init__(self, map_id_to_folders, map_id_to_specs, map_id_to_groups, map_id_to_reqs, root_folder):
        self.map_id_to_folders = map_id_to_folders
        self.map_id_to_specs = map_id_to_specs
        self.map_id_to_groups = map_id_to_groups
        self.map_id_to_reqs = map_id_to_reqs
        self.root_folder = root_folder

    @staticmethod
    def sort_folders_by_name_key(folders):
        def convert(text): int(text) if text.isdigit() else text.lower()
        return list(sorted(
            folders,
            key=lambda name_: [convert(c) for c in re.split('([0-9]+)', name_["name"])]
        ))

    def iterate_folder(self, folder, current_parent_stack=None):
        if current_parent_stack is None:
            current_parent_stack = []
        assert folder is not None

        # Step 1: Yield the folder itself.

        yield folder, "folder", current_parent_stack

        # Step 2: Yield the child folders.

        new_parent_stack = current_parent_stack + [folder]

        children_ids = folder["children"]
        unsorted_children = list(map(lambda ch_id: self.map_id_to_folders[ch_id], children_ids))
        sorted_children = ValispaceDataContainer.sort_folders_by_name_key(unsorted_children)

        for child_folder_ in sorted_children:
            yield from self.iterate_folder(child_folder_, new_parent_stack)

        # Step 3: Print the child specifications.

        folder_specs_ids = folder["items"] if "items" in folder else []
        folder_specs = list(map(
            lambda folder_id: self.map_id_to_specs[folder_id], folder_specs_ids
        ))
        for spec_ in folder_specs:
            yield from self.iterate_spec(spec_, new_parent_stack)

    def iterate_spec(self, spec, current_parent_stack, context=None):
        assert isinstance(current_parent_stack, list)
        if context is None:
            context = ValispaceDataSpecIterationContext()

        assert isinstance(spec, dict)

        # Step 1: Yield the spec itself.

        yield spec, "spec", current_parent_stack

        # Step 2: Yield the child requirements groups.

        new_parent_stack = current_parent_stack + [spec]

        spec_groups_ids = spec["requirement_groups"]
        spec_groups = map(
            lambda group_id: self.map_id_to_groups[group_id], spec_groups_ids
        )

        for child_spec_group_ in spec_groups:
            if child_spec_group_["id"] in context.all_spec_groups:
                continue
            yield from self.iterate_spec_group(child_spec_group_, new_parent_stack, context=context)

        # Step 3: Yield the print requirements.

        requirements_ids = spec["requirements"] if "requirements" in spec else []
        requirements = map(
            lambda requirement_id: self.map_id_to_reqs[requirement_id], requirements_ids
        )

        for requirement_ in requirements:
            if requirement_["id"] in context.all_spec_requirements:
                continue
            yield requirement_, "requirement", new_parent_stack
            context.all_spec_requirements.add(requirement_["id"])

    def iterate_spec_group(self, spec_group, current_parent_stack, context):
        assert isinstance(spec_group, dict)
        assert isinstance(context, ValispaceDataSpecIterationContext)

        if context is None:
            context = ValispaceDataSpecIterationContext()

        # Step 1: Yield the spec group itself.

        yield spec_group, "spec_group", current_parent_stack
        context.all_spec_groups.add(spec_group["id"])

        # Step 2: Yield the child spec groups.

        new_parent_stack = current_parent_stack + [spec_group]

        spec_groups_ids = spec_group["children"]

        for child_spec_group_ in map(
            lambda group_id: self.map_id_to_groups[group_id], spec_groups_ids
        ):
            if child_spec_group_["id"] in context.all_spec_groups:
                continue
            yield from self.iterate_spec_group(child_spec_group_, new_parent_stack, context)

        # Step 3: Yield the child requirements.

        requirements_ids = spec_group["requirements"] if "requirements" in spec_group else []
        requirements = map(
            lambda requirement_id: self.map_id_to_reqs[requirement_id], requirements_ids
        )
        for requirement_ in requirements:
            if requirement_["id"] in context.all_spec_requirements:
                continue
            yield requirement_, "requirement", new_parent_stack
            context.all_spec_requirements.add(requirement_["id"])


class ProjectTreeIterator:
    """
    This example helper class demonstrates how the iteration methods of the
    ValispaceDataContainer class can be used to achieve a complete iteration
    over a Valispace project's requirements tree.

    Below in this __init__ function, the iterator can be extended with extra
    options for what should be iterated or skipped. The iterator function
    can use these options for a customized iteration.
    """

    def iterate(self, container: ValispaceDataContainer):
        folders_iterated = 0
        specs_iterated = 0
        groups_iterated = 0
        requirements_iterated = 0

        reqs_so_far = set()
        for node, node_type, current_stack in container.iterate_folder(container.root_folder):
            print(f"Current node: {node_type} at level: {len(current_stack)} => ", end="")

            if node_type == "folder":
                folders_iterated += 1
                print(f'Folder: {node["name"]}')

            elif node_type == "spec":
                specs_iterated += 1
                print(f'Spec: {node["name"]}')

            elif node_type == "spec_group":
                groups_iterated += 1
                print(f'Spec group: {node["name"]}')

            elif node_type == "requirement":
                if node["id"] not in reqs_so_far:
                    requirements_iterated += 1
                reqs_so_far.add(node["id"])
                requirement_uid = node.get("identifier", "<No identifier>")
                print(f"Requirement: {requirement_uid}")
            else:
                raise AssertionError

        print(f"Iteration results:")
        print(f"Folders: {folders_iterated}")
        print(f"Specs: {specs_iterated}")
        print(f"Groups: {groups_iterated}")
        print(f"Requirements: {requirements_iterated}")

        assert folders_iterated == len(container.map_id_to_folders.values()), container.map_id_to_folders
        assert specs_iterated == len(container.map_id_to_specs.values()), container.map_id_to_specs.values()
        assert groups_iterated == len(container.map_id_to_groups.values()), container.map_id_to_groups
        assert requirements_iterated == len(container.map_id_to_reqs.values()), container.map_id_to_reqs.values()


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

    map_id_to_folders = {}
    map_id_to_specs = {}
    map_id_to_groups = {}
    map_id_to_reqs = {}

    print("FOLDERS")
    result = valispace.get_folders(project_id)
    for entry_ in result:
        map_id_to_folders[entry_["id"]] = entry_
    print(f"FOLDERS: {(result)}")

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

    # The Root of the project can also contain specifications that are not
    # included to any folder. Create an artificial "ROOT" folder that becomes
    # a yet another topmost folder and is after all top-level folders.

    top_level_folders = list(filter(
        lambda folder_: folder_["parent"] is None, map_id_to_folders.values()
    ))
    top_level_folders = ValispaceDataContainer.sort_folders_by_name_key(top_level_folders)
    top_level_folders_ids = list(map(lambda tlf_: tlf_["id"], top_level_folders))

    root_level_specs = filter(
        lambda spec: spec["folder"] is None, map_id_to_specs.values()
    )
    root_level_specs_ids = list(map(
        lambda spec: spec["id"], root_level_specs
    ))
    root_folder = {"id": "ROOT", "name": "ROOT", "items": root_level_specs_ids, "children": top_level_folders_ids}
    map_id_to_folders["ROOT"] = root_folder

    container = ValispaceDataContainer(
        map_id_to_folders=map_id_to_folders,
        map_id_to_specs=map_id_to_specs,
        map_id_to_groups=map_id_to_groups,
        map_id_to_reqs=map_id_to_reqs,
        root_folder=root_folder,
    )

    project_tree_iterator = ProjectTreeIterator()
    project_tree_iterator.iterate(container)


main()