# TEST COMAND EXAMPLES WITH THE SATURN V PROJECT

# Before:
# Saturn V project id should be = 1 (change in example if it isn't)
# In CommandModule.Mass mark impact to LaunchEscapeSystem.Mass
# Tag CommandModule component and CommandModule.Mass with a tag named "test".
# Tag id should be = 1 (change in exampleif it isn't)


import valispace
valispace = valispace.API()

print("\n--- GET VALI ---")
a = valispace.get_vali(id=3)
print("id=3: \n" + str(a))
b = valispace.get_vali(name='CommandModule.Mass')
print("\nname='CommandModule.Mass' \n" + str(b))

print("\n\n--- FILTER VALI ---")
c = valispace.filter_vali(workspace_id=1)
print("workspace_id=1: \n" + str(c))
d = valispace.filter_vali(workspace_name='Default Workspace')
print("\nworkspace_name='Default Workspace' \n" + str(d))
e = valispace.filter_vali(project_id=2)
print("\nproject_id=2: \n" + str(e))
f = valispace.filter_vali(project_name='Saturn_V')
print("\nproject_name='Saturn_V' \n" + str(f))
g = valispace.filter_vali(parent_id=3)
print("\nparent_id=2 \n" + str(g))
f = valispace.filter_vali(parent_name='ApolloSpacecraft')
print("\nparent_name='ApolloSpacecraft' \n" + str(f))
g = valispace.filter_vali(tag_id=1)
print("\ntag_id=1 \n" + str(g))
h = valispace.filter_vali(tag_name='test')
print("\ntag_name='test' \n" + str(h))
i = valispace.filter_vali(vali_marked_as_impacted=4)
print("\nvali_marked_as_impacted=4 \n" + str(i))

del a, b, c, d, e, f, g, h

print("\n--- GET COMPONENT ---")
a = valispace.get_component(id=3)
print("id=3: \n" + str(a))
b = valispace.get_component(unique_name='CommandModule')
print("\nname='CommandModule' \n" + str(b))

print("\n\n--- FILTER COMPONENT ---")
c = valispace.filter_component(workspace_id=1)
print("workspace_id=1: \n" + str(c))
d = valispace.filter_component(workspace_name='Default Workspace')
print("\nworkspace_name='Default Workspace' \n" + str(d))
e = valispace.filter_component(project_id=2)
print("\nproject_id=2: \n" + str(e))
f = valispace.filter_component(project_name='Saturn_V')
print("\nproject_name='Saturn_V' \n" + str(f))
g = valispace.filter_component(parent_id=2)
print("\nparent_id=2 \n" + str(g))
f = valispace.filter_component(parent_name='ApolloSpacecraft')
print("\nparent_name='ApolloSpacecraft' \n" + str(f))
g = valispace.filter_component(tag_id=1)
print("\ntag_id=1 \n" + str(g))
h = valispace.filter_component(tag_name='test')
print("\ntag_name='test' \n" + str(h))


del a, b, c, d, e, f, g, h

print("\n--- GET PROJECT ---")
a = valispace.get_project(id=2)
print("id=2: \n" + str(a))
b = valispace.get_project(name='Saturn_V')
print("\nname='Saturn_V' \n" + str(b))

print("\n\n--- FILTER PROJECT ---")
c = valispace.filter_project(workspace_id=1)
print("workspace_id=1: \n" + str(c))
d = valispace.filter_project(workspace_name='Default Workspace')
print("\nworkspace_name='Default Workspace' \n" + str(d))