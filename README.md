# Valispace Python API

The Valispace python API lets you access and update objects in your Valispace deployment.

## Getting Started

To make use of the Valispace API you must have a valid login to any Valispace deployment. If you don't have an account, you can get a demo account at [demo.valispace.com](https://demo.valispace.com). You can also find further documentation in [docs.valispace.com](http://www.valispace.com/docs/).

### Installing

Install the Valispace python API with pip:

```
pip install valispace
```

### Import the API

Import valispace API module in a python script:

```python
import valispace
```

**And initialize with:**

```python
valispace = valispace.API()
```

At this step you will need to enter your Valispace url (e.g. https://demo.valispace.com), username and password for authentication, or use the one line function:

```python
valispace = valispace.API(url='https://demo.valispace.com', username='your_user_name', password='******')
```

Then use the Valispace API like this:

### GET :

A dict of Valis:
```python
valis = valispace.get_vali_list()
```

**All Vali** ids and names:
```python
all_vali_names = valispace.get_vali_names()
```

A **Vali** with all properties:

Argument | Example
------------- | -------------
id | `valispace.get_vali(id=1)`
unique_name | `valispace.get_vali_by_name(vali_name='Blade', project_name='Fan')`

A **matrix**:

```python
matrix = valispace.get_matrix(id=57)
```

or a condensed version with only Vali ids and values:

```python
matrix = valispace.get_matrix_str(id=57)
```

A **Component** with all properties:

Argument | Example
------------- | -------------
id | `valispace.get_component(id=1)`
unique_name | `valispace.get_component_by_name(unique_name='Fan.Blade', project_name='Fan')`


A **Project** with all properties:

Argument | Example
------------- | -------------
id | `valispace.get_project(id=1)`
name | `valispace.get_project_by_name(name='Fan')`

### FILTER :

List of **Valis** with the specified arguments:

Argument | Example
------------- | -------------
workspace_id | `valispace.get_vali_list(workspace_id=1)`
workspace_name | `valispace.get_vali_list(workspace_name='Default Workspace')`
project_id | `valispace.get_vali_list(project_id=1)`
project_name | `valispace.get_vali_list(project_name='Saturn_V')`
parent_id | `valispace.get_vali_list(parent_id=1)`
parent_name | `valispace.get_vali_list(parent_name='Fan')`
tag_id | `valispace.get_vali_list(tag_id=10)`
tag_name | `valispace.get_vali_list(tag_id='example_tag')`
vali_marked_as_impacted | `valispace.get_vali_list(vali_marked_as_impacted='10')`


List of **Components** with the specified arguments:

Argument | Example
------------- | -------------
workspace_id | `valispace.get_component_list(workspace_id=1)`
workspace_name | `valispace.get_component_list(workspace_name='Default Workspace')`
project_id | `valispace.get_component_list(project_id=1)`
project_name | `valispace.get_component_list(project_name='Fan')`
parent_id | `valispace.get_component_list(parent_id=1)`
parent_name | `valispace.get_component_list(parent_name='Fan')`
tag_id | `valispace.get_component_list(tag_id=10)`
tag_name | `valispace.get_component_list(tag_name='example_tag')`


List of **Projects** with the specified arguments:

Argument | Example
------------- | -------------
workspace_id | `valispace.get_project_list(workspace_id=1)`
workspace_name | `valispace.get_project_list(workspace_name='Default Workspace')`

### UPDATE:
A Vali formula:
```python
valispace.update_vali(id=50, formula=str(value + 1))
```

A matrix:
```python
valispace.update_matrix_formulas(id=57, matrix_formula=[[2.1], [0.0], [0.0]])
```


### POST
```python
valispace.post_data(type='vali', data=json_object)
```

The input data should be a single JSON object. Check the examples:

```python
import valispace
valispace = valispace.API()

# -- Insert new Component --
valispace.post_data(type='component', data="""{
        "name": "component_name",
        "description": "Insert description here",
        "parent": null,
        "project": 25,
        "tags": [30, 31, 32]
    }""")

# -- Insert new Vali --
valispace.post_data(type='vali', data="""{
        "parent": 438,
        "shortname": "mass",
        "description": "",
        "unit": "kg",
        "formula": "5",
        "minimum": null,
        "maximum": null,
        "margin_minus": "0",
        "margin_plus": "0",
        "uses_default_formula": false,
        "reference": "",
        "type": null
    }""")

# -- Insert new Textvali --
valispace.post_data(type='textvali', data="""{
        "shortname": "Message",
        "text": "Message text",
        "parent": 438
    }""")

# -- Insert new Tag --
valispace.post_data(type='tag', data="""{
        "name": "white-tag",
        "color": "#FFFFFF"
    }""")
```
**Notes:**
- The "name" fields should never be repeated, this will result in a error in the REST API.
- The "valis" are automatically updated when new valis with this componenet id are inserted


<!-- ## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us. -->

## Authors

* **Valispace**

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<!-- ## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc -->
