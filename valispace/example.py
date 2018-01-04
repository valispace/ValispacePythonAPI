# TEST COMAND EXAMPLES WITH THE SATURN V PROJECT

# Before:
# Saturn V project id should be = 1 (change in example if it isn't)
# In CommandModule.Mass mark impact to LaunchEscapeSystem.Mass
# Tag CommandModule component and CommandModule.Mass with a tag named "test".
# Tag id should be = 1 (change in exampleif it isn't)


import valispace
vs = valispace.API()

print("\n--- GET VALI ---")
a = vs.get_vali(id=3)
print("id=3: \n" + str(a))
b = vs.get_vali(name='CommandModule.Mass')
print("\nname='CommandModule.Mass' \n" + str(b))

print("\n\n--- FILTER VALI ---")
c = vs.filter_vali(workspace_id=1)
print("workspace_id=1: \n" + str(c))
d = vs.filter_vali(workspace_name='Default Workspace')
print("\nworkspace_name='Default Workspace' \n" + str(d))
e = vs.filter_vali(project_id=2)
print("\nproject_id=2: \n" + str(e))
f = vs.filter_vali(project_name='Saturn_V')
print("\nproject_name='Saturn_V' \n" + str(f))
g = vs.filter_vali(parent_id=3)
print("\nparent_id=2 \n" + str(g))
f = vs.filter_vali(parent_name='ApolloSpacecraft')
print("\nparent_name='ApolloSpacecraft' \n" + str(f))
g = vs.filter_vali(tag_id=1)
print("\ntag_id=1 \n" + str(g))
h = vs.filter_vali(tag_name='test')
print("\ntag_name='test' \n" + str(h))
i = vs.filter_vali(vali_marked_as_impacted=4)
print("\nvali_marked_as_impacted=4 \n" + str(i))
j = vs.filter_vali(workspace_id=1, project_id=2, parent_id=3, tag_id=1, vali_marked_as_impacted=4)
print("\nworkspace_id=1, project_id=2, parent_id=3, tag_id=1, vali_marked_as_impacted=4 \n" + str(i))

del a, b, c, d, e, f, g, h, i, j

print("\n--- GET COMPONENT ---")
a = vs.get_component(id=3)
print("id=3: \n" + str(a))
b = vs.get_component(unique_name='CommandModule')
print("\nname='CommandModule' \n" + str(b))

print("\n\n--- FILTER COMPONENT ---")
c = vs.filter_component(workspace_id=1)
print("workspace_id=1: \n" + str(c))
d = vs.filter_component(workspace_name='Default Workspace')
print("\nworkspace_name='Default Workspace' \n" + str(d))
e = vs.filter_component(project_id=2)
print("\nproject_id=2: \n" + str(e))
f = vs.filter_component(project_name='Saturn_V')
print("\nproject_name='Saturn_V' \n" + str(f))
g = vs.filter_component(parent_id=2)
print("\nparent_id=2 \n" + str(g))
f = vs.filter_component(parent_name='ApolloSpacecraft')
print("\nparent_name='ApolloSpacecraft' \n" + str(f))
g = vs.filter_component(tag_id=1)
print("\ntag_id=1 \n" + str(g))
h = vs.filter_component(tag_name='test')
print("\ntag_name='test' \n" + str(h))
i = vs.filter_vali(workspace_id=1, project_id=2, parent_id=2)
print("\nworkspace_id=1, project_id=2, parent_id=2 \n" + str(i))


del a, b, c, d, e, f, g, h, i

print("\n--- GET PROJECT ---")
a = vs.get_project(id=2)
print("id=2: \n" + str(a))
b = vs.get_project(name='Saturn_V')
print("\nname='Saturn_V' \n" + str(b))

print("\n\n--- FILTER PROJECT ---")
c = vs.filter_project(workspace_id=1)
print("workspace_id=1: \n" + str(c))
d = vs.filter_project(workspace_name='Default Workspace')
print("\nworkspace_name='Default Workspace' \n" + str(d))