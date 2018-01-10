#!/usr/bin/env python2

# TEST COMAND EXAMPLES WITH THE SATURN V PROJECT

# Before:
# Saturn V project id should be = 1 (change in example if it isn't)
# In CommandModule.Mass mark impact to LaunchEscapeSystem.Mass
# Tag CommandModule component and CommandModule.Mass with a tag named "test".
# Tag id should be = 1 (change in exampleif it isn't)

import valispace

vali = valispace.API()

print("\n--- GET VALI ---")
a = vali.get_vali(id=3)
print("id=3: \n" + str(a))
b = vali.get_vali_by_name(vali_name='CommandModule.Mass', project_name='Saturn_V')
print("\nname='CommandModule.Mass' \n" + str(b))

print("\n\n--- GET FILTERED VALI LISTS ---")
c = vali.get_vali_list(workspace_id=1)
print("workspace_id=1: \n" + str(c))
d = vali.get_vali_list(workspace_name='Default Workspace')
print("\nworkspace_name='Default Workspace' \n" + str(d))
e = vali.get_vali_list(project_id=2)
print("\nproject_id=2: \n" + str(e))
f = vali.get_vali_list(project_name='Saturn_V')
print("\nproject_name='Saturn_V' \n" + str(f))
g = vali.get_vali_list(parent_id=3)
print("\nparent_id=2 \n" + str(g))
f = vali.get_vali_list(parent_name='ApolloSpacecraft')
print("\nparent_name='ApolloSpacecraft' \n" + str(f))
g = vali.get_vali_list(tag_id=1)
print("\ntag_id=1 \n" + str(g))
h = vali.get_vali_list(tag_name='test')
print("\ntag_name='test' \n" + str(h))
i = vali.get_vali_list(vali_marked_as_impacted=4)
print("\nvali_marked_as_impacted=4 \n" + str(i))

del a, b, c, d, e, f, g, h

print("\n--- GET COMPONENT ---")
a = vali.get_component(3)
print("id=3: \n" + str(a))
b = vali.get_component_by_name(unique_name='CommandModule', project_name='Saturn_V')
print("\nname='CommandModule' \n" + str(b))

print("\n\n--- GET FILTERED COMPONENT LIST ---")
c = vali.get_component_list(workspace_id=1)
print("workspace_id=1: \n" + str(c))
d = vali.get_component_list(workspace_name='Default Workspace')
print("\nworkspace_name='Default Workspace' \n" + str(d))
e = vali.get_component_list(project_id=2)
print("\nproject_id=2: \n" + str(e))
f = vali.get_component_list(project_name='Saturn_V')
print("\nproject_name='Saturn_V' \n" + str(f))
g = vali.get_component_list(parent_id=2)
print("\nparent_id=2 \n" + str(g))
f = vali.get_component_list(parent_name='ApolloSpacecraft')
print("\nparent_name='ApolloSpacecraft' \n" + str(f))
g = vali.get_component_list(tag_id=1)
print("\ntag_id=1 \n" + str(g))
h = vali.get_component_list(tag_name='test')
print("\ntag_name='test' \n" + str(h))


del a, b, c, d, e, f, g, h

print("\n--- GET PROJECT ---")
a = vali.get_project(id=2)
print("id=2: \n" + str(a))
b = vali.get_project_by_name(name='Saturn_V')
print("\nname='Saturn_V' \n" + str(b))

print("\n\n--- GET FILTERED PROJECT LIST ---")
c = vali.get_project_list(workspace_id=1)
print("workspace_id=1: \n" + str(c))
d = vali.get_project_list(workspace_name='Default Workspace')
print("\nworkspace_name='Default Workspace' \n" + str(d))
